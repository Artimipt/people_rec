import cv2
import torch

def yolo_people_boxes(results):
    people_boxes = []
    confidences = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls.item())
            if cls_id == 0:  # COCO class ID for 'person'
                people_boxes.append(box)
                confidences.append(float(box.conf.item()))

    return people_boxes, confidences

def detect(video_path: str, output_path: str, model, model_type: str):

    if isinstance(model, torch.nn.Module):
        model.eval()

    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if model_type == "yolo":
            results = model(frame)
            people_boxes, confidences = yolo_people_boxes(results)

        elif model_type == "rf-detr":
            results = model.predict(frame, threshold=0.5)
            people_boxes = results.xyxy
            confidences = results.confidence

        annotated_frame = frame.copy()
        for i, box in enumerate(people_boxes):
            if model_type == "yolo":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
            else:  
                x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f'Person {confidences[i]:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(annotated_frame)
    cap.release()
    out.release()



