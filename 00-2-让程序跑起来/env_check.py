import os
import platform
import shutil
import subprocess
from pathlib import Path


def check_command(label, command):
    """Return one concise status line for an installed command."""
    executable = shutil.which(command[0])
    if executable is None:
        return f"{label}：未检测到（命令 {command[0]} 不在 PATH 中）"

    try:
        result = subprocess.run(
            [executable, *command[1:]],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        output = (result.stdout or result.stderr).strip().splitlines()
        version = output[0] if output else f"已检测到，退出代码 {result.returncode}"
        return f"{label}：已检测到，版本 {version}"
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"{label}：已找到命令，但读取版本失败（{error.__class__.__name__}）"


def find_vscode():
    """Check the VS Code command and common Windows installation paths."""
    executable = shutil.which("code") or shutil.which("code.cmd")
    if executable:
        return executable

    candidates = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("PROGRAMFILES")
    program_files_x86 = os.environ.get("PROGRAMFILES(X86)")

    if local_app_data:
        candidates.append(os.path.join(local_app_data, "Programs", "Microsoft VS Code", "Code.exe"))
    if program_files:
        candidates.append(os.path.join(program_files, "Microsoft VS Code", "Code.exe"))
    if program_files_x86:
        candidates.append(os.path.join(program_files_x86, "Microsoft VS Code", "Code.exe"))

    return next((path for path in candidates if os.path.isfile(path)), None)


report_lines = [
    f"主机名：{platform.node() or '未能读取'}",
    f"Python：已运行，版本 {platform.python_version()}",
    check_command("Git", ["git", "--version"]),
    check_command("Node.js", ["node", "--version"]),
]

vscode = find_vscode()
if vscode:
    if vscode.lower().endswith(".cmd"):
        report_lines.append(check_command("VS Code", ["cmd", "/c", vscode, "--version"]))
    else:
        report_lines.append(check_command("VS Code", [vscode, "--version"]))
else:
    report_lines.append("VS Code：未检测到；请手动确认是否安装")

print("=== 课程开发环境检查 ===")
for line in report_lines:
    print(line)

report_path = Path(__file__).resolve().parent / "环境检测报告.md"
report_content = "# 环境检测报告\n\n" + "\n".join(f"- {line}" for line in report_lines) + "\n"
report_path.write_text(report_content, encoding="utf-8")
print(f"检测报告已写入：{report_path.name}")

print(f"环境检测完成，共检测 {len(report_lines)} 项。")
