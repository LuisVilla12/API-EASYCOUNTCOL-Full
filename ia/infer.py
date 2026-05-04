import os
import pandas as pd
import torch
import cv2
import csv
import numpy as np
from ultralytics import YOLO
from collections import Counter
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

# ================================
# CONFIG
# ================================
MODEL_PATH = "ia/YOLO/1_Y12/weights/best.pt"
IMG_SIZE = 1024

model = YOLO(MODEL_PATH)
FEATURE_MAP = None
BASE = ""

# ================================
# HOOK
# ================================
def hook_fmap(module, input, output):
    global FEATURE_MAP
    FEATURE_MAP = output

# Registrar hook
layer = model.model.model[17]
layer.register_forward_hook(hook_fmap)

# ================================
# DESCRIPTOR
# ================================
def extract_descriptor(box, fmap, img_shape):
    H_img, W_img = img_shape
    _, C, Hf, Wf = fmap.shape

    x0, y0, x1, y1 = map(float, box)

    sx0 = int((x0 / W_img) * Wf)
    sy0 = int((y0 / H_img) * Hf)
    sx1 = int((x1 / W_img) * Wf)
    sy1 = int((y1 / H_img) * Hf)

    sx0 = max(0, min(Wf - 1, sx0))
    sy0 = max(0, min(Hf - 1, sy0))
    sx1 = max(sx0 + 1, min(Wf, sx1))
    sy1 = max(sy0 + 1, min(Hf, sy1))

    crop = fmap[0, :, sy0:sy1, sx0:sx1]

    if crop.numel() == 0:
        cx = min(max((sx0 + sx1) // 2, 0), Wf - 1)
        cy = min(max((sy0 + sy1) // 2, 0), Hf - 1)
        return fmap[0, :, cy, cx].cpu().numpy()

    return crop.mean(dim=(1, 2)).cpu().numpy()

# ================================
# VECTOR DE CARACTERÍSTICAS
# ================================
def vector_caracteristicas(img_name):
    global FEATURE_MAP

    FEATURE_MAP = None

    full_path = os.path.join("ia/resultados/img/", img_name)

    img = cv2.imread(full_path)
    if img is None:
        raise FileNotFoundError(f"No se encontró la imagen: {img_name}")

    H_img, W_img = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # =========================
    # 1. DETECCIÓN (CORRECTA)
    # =========================
    results = model.predict(
        source=full_path,   # 🔥 CLAVE
        conf=0.2,
        iou=0.5,
        imgsz=IMG_SIZE,
        verbose=False
    )

    boxes = results[0].boxes.xyxy.cpu().numpy()
    print("🔍 Detectados:", len(boxes))

    if len(boxes) == 0:
        return 0

    # =========================
    # 2. FEATURE MAP (ALINEADO)
    # =========================
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))

    tensor = torch.from_numpy(img_resized.astype(np.float32) / 255.0)\
        .permute(2, 0, 1).unsqueeze(0).to(model.device)

    with torch.no_grad():
        _ = model.model(tensor)

    print("FEATURE_MAP:", FEATURE_MAP.shape if FEATURE_MAP is not None else None)

    if FEATURE_MAP is None:
        raise RuntimeError("❌ FEATURE_MAP no generado")

    # =========================
    # 3. DESCRIPTORES
    # =========================
    csv_rows = []

    for idx, box in enumerate(boxes):
        desc = extract_descriptor(box, FEATURE_MAP, (IMG_SIZE, IMG_SIZE))

        row = [
            idx,
            int(box[0]), int(box[1]),
            int(box[2]), int(box[3])
        ] + desc.tolist()

        csv_rows.append(row)

    # Guardar CSV
    C = FEATURE_MAP.shape[1]
    header = ["id", "x0", "y0", "x1", "y1"] + [f"f{i}" for i in range(C)]

    os.makedirs("ia/resultados/cvs", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(img_name))[0]
    csv_path = f"ia/resultados/cvs/{base_name}.csv"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(csv_rows)

    return len(boxes)

# ================================
# CLUSTERING
# ================================
def detect_optimal_clusters(X, max_clusters=4):
    if X.shape[0] < 2:
        return 1

    best_k = 1
    best_score = -1

    for k in range(2, min(max_clusters, X.shape[0]) + 1):
        try:
            labels = AgglomerativeClustering(n_clusters=k).fit_predict(X)
            if len(set(labels)) < 2:
                continue
            score = silhouette_score(X, labels)
            if score > best_score:
                best_score = score
                best_k = k
        except:
            continue

    return best_k

def tratamiento_imagen(name_image):
    global BASE
    BASE = os.path.splitext(name_image)[0]

    count = vector_caracteristicas(name_image)

    if count == 0:
        return {
            "image_resultado": None,
            "labels": 0,
            "optimal_clusters": 0,
            "clustersDetail": "{}"
        }

    return clustering(name_image, count)

def clustering(name_image, count):
    CSV_PATH = f"ia/resultados/cvs/{BASE}.csv"
    OUT_PATH = f"ia/resultados/clustering_img/{BASE}.jpg"

    df = pd.read_csv(CSV_PATH)

    cols = [c for c in df.columns if c.startswith("f")]
    X = df[cols].values

    X = StandardScaler().fit_transform(X)

    n_components = min(40, X.shape[0], X.shape[1])
    X = PCA(n_components=n_components).fit_transform(X)

    k = detect_optimal_clusters(X)

    labels = np.zeros(len(X)) if k == 1 else AgglomerativeClustering(n_clusters=k).fit_predict(X)

    conteo = dict(Counter(labels))
    total = sum(conteo.values())

    clusters_info = {
        int(k): {
            "count": int(v),
            "percentage": round((v / total) * 100, 2)
        }
        for k, v in conteo.items()
    }

    img = cv2.imread(os.path.join("ia/resultados/img/", name_image))

    colors = [(0,0,255),(255,0,0),(0,255,0),(0,255,255)]

    for i, row in df.iterrows():
        x0, y0, x1, y1 = map(int, [row["x0"], row["y0"], row["x1"], row["y1"]])
        color = colors[int(labels[i]) % len(colors)]
        cv2.rectangle(img, (x0,y0), (x1,y1), color, 1)

    os.makedirs("ia/resultados/clustering_img", exist_ok=True)
    cv2.imwrite(OUT_PATH, img)

    return {
        "image_resultado": img,
        "labels": int(count),
        "optimal_clusters": int(k),
        "clustersDetail": json.dumps(clusters_info)
    }