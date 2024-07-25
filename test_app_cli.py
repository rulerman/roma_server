import cv2
import warnings
import numpy as np
from pathlib import Path
from hloc import logger
from ui.utils import (
    get_matcher_zoo,
    load_config,
    DEVICE,
    ROOT,
)
from ui.api import ImageMatchingAPI


def test_one(filepath1, filepath2,max_keypoints=1000, match_threshold=0.2):
    # Validate max_keypoints
    if not (1000 <= max_keypoints <= 10000):
        raise ValueError("max_keypoints must be between 1000 and 10000")

    # Validate match_threshold
    if not (0 <= match_threshold <= 1):
        raise ValueError("match_threshold must be between 0 and 1")

    # img_path1 = ROOT / "datasets/sacre_coeur/mapping/27_1_1712651922_257.jpg"
    # img_path2 = ROOT / "datasets/sacre_coeur/mapping/27_1_1712701850_268.JPG"
    img_path1 = ROOT / filepath1
    img_path2 = ROOT / filepath2
    image0 = cv2.imread(str(img_path1))[:, :, ::-1]  # RGB
    image1 = cv2.imread(str(img_path2))[:, :, ::-1]  # RGB

    # dense
    conf = {
        "matcher": {
             "output": "matches-roma",
        "model": {
            "name": "roma",
            "weights": "outdoor",
            "max_keypoints": max_keypoints,
            "match_threshold": match_threshold,
        },
        "preprocessing": {
            "grayscale": False,
            "force_resize": True,
            "resize_max": 1024,
            "width": 320,
            "height": 240,
            "dfactor": 8,
        },
            "max_error": 1,
            "cell_size": 1,
        },
        "dense": True,
    }

    api = ImageMatchingAPI(conf=conf, device=DEVICE)
    api(image0, image1)
    print('api done')
    log_path = ROOT / "output"
    log_path.mkdir(exist_ok=True, parents=True)
    api.visualize(log_path=log_path)
    print('visualize image done')
    return 0


if __name__ == "__main__":
    config = load_config(ROOT / "ui/config.yaml")
    img_path1 = "input/27_1_1712701850_268.JPG"
    img_path2 = "input/27_1_1712701877_269.JPG"
    test_one(img_path1,img_path2)
   # test_all(config)
