import os
from pathlib import Path

def generate_md_index(root_dir: str = ".", output_file: str = "README.md"):
    root_path = Path(root_dir).resolve()
    index_content = []
    
    index_content.append("# Desynk | 众创易享")
    index_content.append("### 文档索引")
    index_content.append("")
    
    processed_folders = set()

    def get_relative_path(file_path: Path) -> str:
        rel_path = file_path.relative_to(root_path)
        return str(rel_path).replace("\\", "/")

    def add_folder_index(folder_path: Path, level: int):
        if folder_path in processed_folders:
            return
        processed_folders.add(folder_path)
        
        indent = "  " * (level - 1)
        rel_path = get_relative_path(folder_path)
        folder_name = folder_path.name
        index_content.append(f"{indent}- [{folder_name}]({rel_path}/)")

    for file_path in sorted(root_path.rglob("*.md")):
        if file_path.name == output_file:
            continue
        
        rel_file_path = get_relative_path(file_path)
       
        path_parts = rel_file_path.split("/")
        
        current_folder = root_path
        for level, part in enumerate(path_parts[:-1], 1):
            current_folder = current_folder / part
            add_folder_index(current_folder, level)
        
        file_level = len(path_parts) 
        file_indent = "  " * (file_level - 1)
        file_name = file_path.stem
        index_content.append(f"{file_indent}- [{file_name}]({rel_file_path})")
        index_content.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(index_content))
    
    print(f"✅ 文档索引已生成完成！输出文件：{os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_md_index()