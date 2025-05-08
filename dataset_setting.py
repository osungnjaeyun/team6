import os

labels_dirs = [
    '/Users/shin/capstone/ultralytics/BabyFinder/test/labels',
    '/Users/shin/capstone/ultralytics/BabyFinder/train/labels',
    '/Users/shin/capstone/ultralytics/BabyFinder/valid/labels'
]

total_deleted = 0

for labels_dir in labels_dirs:
    for file_name in os.listdir(labels_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(labels_dir, file_name)

            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            deleted_count = 0

            for line in lines:
                class_id = line.strip().split(' ')[0]
                if class_id == '3':  # 3번 클래스(stroller) 삭제
                    deleted_count += 1
                else:
                    new_lines.append(line)

            if deleted_count > 0:
                print(f"🗑️ {file_name}: {deleted_count}줄 stroller 삭제됨")
                total_deleted += deleted_count

            with open(file_path, 'w') as f:
                f.writelines(new_lines)

print(f"\n✅ 전체 {total_deleted}개의 stroller 객체 삭제 완료!")