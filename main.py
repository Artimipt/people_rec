import cv2
import argparse
import ultralytics
from src import test_performance, detect
from pathlib import Path
from rfdetr import RFDETRBase


current_dir = Path(__file__).parent
data_dir = current_dir / "data"
output_dir = current_dir / "output"
models_dir = current_dir / "models"


def parse_args():
    parser = argparse.ArgumentParser(description="People recognition")
    parser.add_argument("--input", type=str, default= str(data_dir / "crowd.mp4"))
    parser.add_argument("--output", type=str, default= str(output_dir / "crowd_detected.mp4"))
    parser.add_argument("--model_type", "-m", type=str, default="rf-detr")
    parser.add_argument("--mode", type=str, default="inference")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Model type: {args.model_type}")

    if not Path(args.input).exists():
        raise FileNotFoundError(f"Input file {args.input} not found")
    if not Path(args.output).parent.exists():
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    if args.model_type == "yolo":
        model_path = models_dir / "yolo11n.pt"
        model = ultralytics.YOLO(str(model_path))
    elif args.model_type == "rf-detr":
        model = RFDETRBase()
    else:
        raise ValueError(f"Model type {args.model_type} not supported")

    if args.mode == "inference":
        detect(args.input, args.output, model, model_type=args.model_type)
    elif args.mode == "performance":
        test_performance(detect, results_file=str(output_dir / "performance_results.json"), 
                         num_runs=10, video_path=str(args.input), output_path=str(args.output), model=model, model_type=args.model_type)
    else:
        raise ValueError(f"Mode {args.mode} not supported")