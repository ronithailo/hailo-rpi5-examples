# tests/test_edge_cases.py
import pytest
import subprocess


def run_pipeline_with_input(script, input_source):
    """Helper to run a pipeline script with a specific input."""
    process = subprocess.run(['python', f'basic_pipelines/{script}', '--input', input_source],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def test_invalid_video_input():
    """Test invalid video input."""
    script = 'detection.py'
    result = run_pipeline_with_input(script, 'invalid_path.mp4')
    assert "No such file" in result.stdout, "The pipeline should report an error for an invalid video path."

def test_unsupported_format():
    """Test unsupported input file format."""
    script = 'detection.py'
    result = run_pipeline_with_input(script, 'tests/test_resources/dummy_text.txt')
    assert "Can't typefind stream" in result.stdout, "The pipeline should report an error for unsupported input format."


@pytest.mark.parametrize("script", ["detection.py", "pose_estimation.py", "instance_segmentation.py", "face_recognition.py"])
def test_invalid_command_arguments(script):
    """Test how pipelines handle invalid command-line arguments."""
    process = subprocess.run(['python', f'basic_pipelines/{script}', '--unknown_arg'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert "error: unrecognized arguments:" in process.stderr or "usage:" in process.stderr, \
        "Pipeline did not handle invalid command-line arguments correctly."
