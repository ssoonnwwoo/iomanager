import subprocess
import os
import pyseq

def exr_to_jpg(input_exr_path, output_jpg_path):
    """
    ffmpeg을 사용해 EXR 파일을 JPG로 변환
    Args:
        input_exr_path: 원본 EXR 파일 경로
        output_jpg_path: 출력 JPG 파일 경로
    Returns:
        bool: 변환 성공 여부
    """

    if not os.path.isfile(input_exr_path):
        print(f"[ERROR] EXR does not exist: {input_exr_path}")
        return False

    try:
        cmd = ["ffmpeg", "-y", "-i", input_exr_path, "-q:v", "2", output_jpg_path]
        subprocess.run(cmd, check=True)
        print(f"[COMPLETE] Input : {input_exr_path}")
        print(f"[COMPLETE] Output : {output_jpg_path}")
        return True

    # subprocess에서 run 실패
    except Exception as e:
        print(f"[EXCEPTION] Error occurred while attempting to convert thumbnail: {e}")
        return False


def mov_to_jpg(input_mov_path, output_jpg_path, all_frames=False):
    """
    ffmpeg을 사용해 MOV 파일에서 JPG 이미지 추출
    Args:
        input_mov_path: 원본 MOV 파일 경로
        output_jpg_path: 출력 JPG 경로 (첫 프레임일 경우는 파일, 시퀀스일 경우는 폴더/image_%04d.jpg 형식)
        all_frames (bool): True면 전체 프레임 시퀀스 저장, False면 첫 프레임만 저장
    Returns:
        bool: 추출 성공 여부
    """

    if not os.path.isfile(input_mov_path):
        print(f"[ERROR] MOV does not exist: {input_mov_path}")
        return False

    try:
        cmd = ["ffmpeg", "-y", "-i", input_mov_path]
        
        if all_frames:
            # 전체 프레임 추출
            os.makedirs(os.path.dirname(output_jpg_path), exist_ok=True)
            cmd += ["-q:v", "2", os.path.join(output_jpg_path, "image_%04d.jpg")]
        else:
            # 첫 프레임만 추출
            cmd += ["-frames:v", "1", "-q:v", "2", output_jpg_path]

        subprocess.run(cmd, check=True)
        print(f"[COMPLETE] Input : {input_mov_path}")
        print(f"[COMPLETE] Output : {output_jpg_path}")
        return True

    except Exception as e:
        print(f"[EXCEPTION] Error occurred while extracting JPG from MOV: {e}")
        return False

def mov_to_exrs(mov_path, output_dir):
    print(f"mov: {mov_path}")
    print(f"exrs: {output_dir}")
    parts = output_dir.strip("/").split("/")
    seq_shot = parts[-4]  # "S038_0020"
    typ = parts[-2]       # "org"
    ver = parts[-1]       # "v001"
    # S040_0020_org_v001.######.exr
    
    output_pattern = os.path.join(
        output_dir, f"{seq_shot}_{typ}_{ver}.%06d.exr"
    )

    try:
        cmd = ["ffmpeg", "-y", "-i", mov_path, "-c:v", "exr", output_pattern]
        subprocess.run(cmd, check=True)
        print(f"[COMPLETE] MOV to EXR: {output_pattern}")
        return True
    except Exception as e:
        print(f"[EXCEPTION] Error converting MOV to EXR: {e}")
        return False


def exrs_to_jpgs(src_dir, dest_dir):
    print(f"exrs: {src_dir}")
    print(f"jpgs: {dest_dir}")
    # if not os.path.isdir(src_dir):
    #     print(f"[ERROR] Source directory does not exist: {src_dir}")
    #     return False
    
    # converted_count = 0

    # for root, dirs, seqs in pyseq.walk(src_dir):
    #     for seq in seqs:
    #         ext = seq.ext.lower()
    #         if  ext not in [".exr", ".mov"]:
    #             continue

    #         for frame in seq:
    #             src_path = frame.path

    #             if ext == ".exr":
    #                 base_name = os.path.splitext(os.path.basename(src_path))[0]
    #                 jpg_name = base_name + ".jpg"
    #                 jpg_path = os.path.join(dest_dir, jpg_name)

    #                 success = exr_to_jpg(src_path, jpg_path)
    #                 if success:
    #                     converted_count += 1

    #             elif ext ==".mov":
    #                 mov_file_name = os.path.splitext