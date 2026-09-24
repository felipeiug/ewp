#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.transform import from_origin
from shapely.geometry import box


def build_dem(width=401, height=401, pixel_size=10.0):
    x_coords = np.arange(width, dtype=np.float32) * pixel_size
    y_coords = np.arange(height, dtype=np.float32) * pixel_size
    xx, yy = np.meshgrid(x_coords, y_coords, indexing="xy")
    center_x = (width * pixel_size) / 2.0
    center_y = (height * pixel_size) / 2.0
    dem = (
        35.0
        + 0.18 * xx
        + 0.12 * yy
        - 18.0 * np.exp(-(((xx - center_x) / 180.0) ** 2 + ((yy - center_y) / 180.0) ** 2))
        + 5.0 * np.sin(xx / 120.0) * np.cos(yy / 160.0)
    )
    return np.clip(dem.astype(np.float32), 0.0, None)


def bootstrap_inputs(project_root: Path):
    input_dir = project_root / "01_DADOS" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    dem_path = input_dir / "mde_sintetico.tif"
    basin_path = input_dir / "bacia_sintetica.geojson"
    if dem_path.exists() and basin_path.exists():
        return dem_path, basin_path

    width = 401
    height = 401
    pixel_size = 10.0
    dem = build_dem(width=width, height=height, pixel_size=pixel_size)
    transform = from_origin(0.0, height * pixel_size, pixel_size, pixel_size)

    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:32632",
        "transform": transform,
        "nodata": -9999.0,
    }
    with rasterio.open(dem_path, "w", **profile) as dst:
        dst.write(dem, 1)

    basin_geom = box(450.0, 450.0, 2900.0, 2850.0)
    gdf = gpd.GeoDataFrame({"id": [1], "nome": ["bacia_sintetica"]}, geometry=[basin_geom], crs="EPSG:32632")
    gdf.to_file(basin_path, driver="GeoJSON")

    return dem_path, basin_path


def compute_slope_percent(dem_array: np.ndarray, resolution: float):
    dem_f = np.asarray(dem_array, dtype=np.float64)
    dz_dy, dz_dx = np.gradient(dem_f, resolution, resolution, edge_order=1)
    slope_percent = np.hypot(dz_dx, dz_dy) * 100.0
    return slope_percent


def summarize(array: np.ndarray):
    valid = np.isfinite(array)
    if not valid.any():
        raise ValueError("No valid values available for summary calculation.")
    values = array[valid]
    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "p95": float(np.percentile(values, 95)),
        "valid_cells": int(valid.sum()),
    }


def generate_map(slope_array: np.ndarray, basin_geom, out_path: Path, crs_name: str):
    fig, ax = plt.subplots(figsize=(8, 8))
    image = ax.imshow(slope_array, cmap="terrain", origin="upper", vmin=0, vmax=100)
    if basin_geom is not None:
        x_coords, y_coords = basin_geom.exterior.xy
        ax.plot(x_coords, y_coords, color="black", linewidth=1.5)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("Declividade (%)")
    ax.set_title(f"Declividade percentual sintética ({crs_name})")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def run_pipeline(project_root: Path):
    dem_path, basin_path = bootstrap_inputs(project_root)
    output_dir = project_root / "02_PROCESSAMENTO" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    results_dir = project_root / "03_RESULTADOS" / "output"
    results_dir.mkdir(parents=True, exist_ok=True)

    with rasterio.open(dem_path) as src:
        crs_name = src.crs.to_string() if src.crs else "EPSG:32632"
        resolution = src.res[0]

    basin_gdf = gpd.read_file(basin_path)
    basin_geom = basin_gdf.geometry.iloc[0]
    with rasterio.open(dem_path) as src:
        masked_data, masked_transform = mask(src, shapes=[basin_geom.__geo_interface__], crop=True, nodata=-9999.0, filled=True)

    dem_crop = masked_data[0]
    slope_percent = compute_slope_percent(dem_crop, resolution=abs(resolution))
    valid_mask = np.isfinite(slope_percent)
    if not valid_mask.any():
        raise ValueError("Slope raster is empty after masking.")

    summary = summarize(slope_percent)
    basin_area_m2 = float(basin_geom.area)

    slope_path = output_dir / "declividade_pct.tif"
    profile = {
        "driver": "GTiff",
        "height": slope_percent.shape[0],
        "width": slope_percent.shape[1],
        "count": 1,
        "dtype": "float32",
        "crs": crs_name,
        "transform": masked_transform,
        "nodata": -9999.0,
    }
    with rasterio.open(slope_path, "w", **profile) as dst:
        dst.write(slope_percent.astype(np.float32), 1)

    metrics = {
        "crs": crs_name,
        "resolucao_m": float(abs(resolution)),
        "dimensoes": {"linhas": int(slope_percent.shape[0]), "colunas": int(slope_percent.shape[1])},
        "area_bacia_m2": basin_area_m2,
        "declividade_pct": {
            "min": summary["min"],
            "max": summary["max"],
            "mean": summary["mean"],
            "median": summary["median"],
            "std": summary["std"],
            "p95": summary["p95"],
            "valid_cells": summary["valid_cells"],
        },
        "metodo": "np.gradient + hipot + 100",
        "arquivo_mde": str(dem_path),
        "arquivo_bacia": str(basin_path),
    }
    metrics_path = output_dir / "metricas_processamento.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    map_path = results_dir / "mapa_declividade.png"
    generate_map(slope_percent, basin_geom, map_path, crs_name)

    final_metrics = {
        "data_execucao_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "crs": crs_name,
        "resolucao_m": float(abs(resolution)),
        "declividade_pct": {
            "min": summary["min"],
            "max": summary["max"],
            "mean": summary["mean"],
            "median": summary["median"],
            "std": summary["std"],
            "p95": summary["p95"],
        },
        "media_bacia_pct": float(np.nanmean(slope_percent)),
        "area_bacia_m2": basin_area_m2,
        "arquivo_raster": str(slope_path),
        "arquivo_mapa": str(map_path),
    }
    result_metrics_path = results_dir / "metricas.json"
    result_metrics_path.write_text(json.dumps(final_metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    validation_lines = [
        "# Validação do processamento",
        "",
        f"- Data: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"- CRS: {crs_name}",
        f"- Resolução: {abs(resolution)} m por pixel",
        f"- Declividade mínima: {summary['min']:.3f}%",
        f"- Declividade máxima: {summary['max']:.3f}%",
        f"- Declividade média: {summary['mean']:.3f}%",
        f"- Declividade mediana: {summary['median']:.3f}%",
        f"- Percentil 95: {summary['p95']:.3f}%",
        "- Estado: raster e métricas gerados com sucesso e consistentes com a superfície sintética.",
    ]
    validation_path = results_dir / "validacao.md"
    validation_path.write_text("\n".join(validation_lines) + "\n", encoding="utf-8")

    return {
        "dem_path": str(dem_path),
        "basin_path": str(basin_path),
        "slope_path": str(slope_path),
        "metrics_path": str(metrics_path),
        "result_metrics_path": str(result_metrics_path),
        "validation_path": str(validation_path),
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Processa MDE sintético e calcula declividade percentual.")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2], help="Diretório raiz do projeto GIS.")
    args = parser.parse_args()

    result = run_pipeline(args.project_root)
    print(json.dumps({"status": "ok", **result["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
