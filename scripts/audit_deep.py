import os
import sys
import inspect
import sqlite3
from pathlib import Path

root = Path(r"c:\Users\ajaya\Desktop\Agro")
sys.path.insert(0, str(root))

print("=== 1. PREPROCESSING CODE INSPECTION ===")
import src.preprocessing.validator as pv
import src.preprocessing.preprocessor as pp
import src.preprocessing.duplicate_detector as pd

print(f"Validator: {pv.__file__}")
for name, obj in inspect.getmembers(pv):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == pv.__name__:
        print(f"  {name} ({type(obj).__name__})")

print(f"Preprocessor: {pp.__file__}")
for name, obj in inspect.getmembers(pp):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == pp.__name__:
        print(f"  {name} ({type(obj).__name__})")

print(f"Duplicate Detector: {pd.__file__}")
for name, obj in inspect.getmembers(pd):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == pd.__name__:
        print(f"  {name} ({type(obj).__name__})")


print("\n=== 2. FEATURE EXTRACTION CODE INSPECTION ===")
import src.feature_extraction.color_features as cf
import src.feature_extraction.texture_features as tf
import src.feature_extraction.shape_features as sf
import src.feature_extraction.pipeline as fp

print(f"Color: {cf.__file__}")
for name, obj in inspect.getmembers(cf):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == cf.__name__:
        print(f"  {name}")

print(f"Texture: {tf.__file__}")
for name, obj in inspect.getmembers(tf):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == tf.__name__:
        print(f"  {name}")

print(f"Shape: {sf.__file__}")
for name, obj in inspect.getmembers(sf):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == sf.__name__:
        print(f"  {name}")

print(f"Pipeline: {fp.__file__}")
for name, obj in inspect.getmembers(fp):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == fp.__name__:
        print(f"  {name}")


print("\n=== 3. WAREHOUSE & SCHEMA CODE INSPECTION ===")
import src.warehouse.models as wm
import src.warehouse.connection as wc
import src.warehouse.schema_manager as ws

print(f"Models: {wm.__file__}")
for name, obj in inspect.getmembers(wm):
    if inspect.isclass(obj) and obj.__module__ == wm.__name__:
        print(f"  {name} (Table: {getattr(obj, '__tablename__', None)})")

print(f"Connection: {wc.__file__}")
for name, obj in inspect.getmembers(wc):
    if inspect.isfunction(obj) and obj.__module__ == wc.__name__:
        print(f"  {name}")

print(f"Schema Manager: {ws.__file__}")
for name, obj in inspect.getmembers(ws):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == ws.__name__:
        print(f"  {name}")


print("\n=== 4. ETL CODE INSPECTION ===")
import src.etl.extract as ee
import src.etl.transform as et
import src.etl.load as el
import src.etl.pipeline as ep

print(f"Extract: {ee.__file__}")
for name, obj in inspect.getmembers(ee):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == ee.__name__:
        print(f"  {name}")

print(f"Transform: {et.__file__}")
for name, obj in inspect.getmembers(et):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == et.__name__:
        print(f"  {name}")

print(f"Load: {el.__file__}")
for name, obj in inspect.getmembers(el):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == el.__name__:
        print(f"  {name}")

print(f"ETL Pipeline: {ep.__file__}")
for name, obj in inspect.getmembers(ep):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == ep.__name__:
        print(f"  {name}")


print("\n=== 5. OLAP CODE INSPECTION ===")
import src.olap.engine as oe
print(f"OLAP Engine: {oe.__file__}")
for name, obj in inspect.getmembers(oe):
    if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == oe.__name__:
        print(f"  {name}")

eng = oe.OLAPEngine()
print("\nOLAP Operations execution:")
print("1. Roll-up:")
print(eng.roll_up())

print("\n2. Drill-down:")
print(eng.drill_down())

print("\n3. Diagnostic Drill-across:")
print(eng.diagnostic_breakdown())

print("\n4. Slice:")
print(eng.slice_crop(crop_name="Rice"))

print("\n5. Dice:")
print(eng.dice(crop_names=["Rice"], pathogen_types=["Fungal", "Bacterial"], min_contrast=0.10))

print("\n6. Pivot:")
print(eng.pivot_crop_by_pathogen())
