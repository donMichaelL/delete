import os


def test_create_file(tmp_path, setup_imports):
    """Check the create_file function correctly creates a file with the given
    content at the specified path."""
    from theTrial.cli import create_file

    path = tmp_path / "fake_dir"
    filename = "fake_file.txt"
    content = "fake_content"
    create_file(path, filename, content)
    assert path.exists()
    file_path = path / filename
    assert file_path.exists()
    assert file_path.read_text() == content


def test_start_command(tmp_path, mocker, setup_imports):
    """Check the start command initializes the correct project structure
    with the expected files."""
    from theTrial.cli import start

    os.chdir(tmp_path)
    start.callback(name="test_app")
    assert (tmp_path / "test_app.py").exists()
    assert (tmp_path / "settings.py").exists()
    assert (tmp_path / "models" / "__init__.py").exists()
    assert (tmp_path / "models" / "models.py").exists()


def test_settings_file_creation_and_content(tmp_path, setup_imports):
    """Test the start command creates a settings.py file with the correct content."""
    from theTrial.cli import start, SETTINGS_INITIAL_CONTENT

    os.chdir(tmp_path)
    start.callback(name="test_app")
    settings_file_path = tmp_path / "settings.py"
    assert settings_file_path.exists()
    with open(settings_file_path) as file:
        content = file.read()
        assert content == SETTINGS_INITIAL_CONTENT


def test_settings_file_creation(tmp_path, setup_imports):
    """Test the start command creates the models.py files with the correct content."""
    from theTrial.cli import start, MODELS_INITIAL_CONTENT

    os.chdir(tmp_path)
    start.callback(name="test_app")
    models_file_path = tmp_path / "models" / "models.py"
    assert models_file_path.exists()
    with open(models_file_path) as file:
        content = file.read()
        assert content == MODELS_INITIAL_CONTENT


def test_file_creation_with_name_argument(tmp_path, setup_imports):
    """Test the start command when provided with the --name argument."""
    from theTrial.cli import start

    os.chdir(tmp_path)
    custom_name = "custom_app"
    start.callback(name=custom_name)
    custom_file_path = tmp_path / f"{custom_name}.py"
    assert custom_file_path.exists()
