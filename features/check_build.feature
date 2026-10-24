Feature: Check AWS Glue Toolkit job buildability and dependencies
  As a developer maintaining AWS Glue jobs
  I want pre-commit to check that the job builds successfully
  So that invalid configurations and broken dependencies are caught before commit

  Scenario: Valid GTK project builds successfully without leaving temporary build files
    Given aws-glue-toolkit builds jobs successfully
    And a pyproject.toml file with content:
      """toml
      [project]
      name = "my-glue-job"
      version = "0.1.0"
      dependencies = ["requests>=2.31.0"]

      [tool.aws-glue-toolkit]
      glue_version = "5.1"
      source = "src"
      script = "__main__.py"
      """
    When I run gtk-check-build on the file
    Then the hook should exit with success
    And no temporary build files should remain in the project directory

  Scenario: Invalid GTK project fails without leaving temporary build files
    Given aws-glue-toolkit fails to build the job
    And a pyproject.toml file with content:
      """toml
      [project]
      name = "broken-glue-job"
      version = "0.1.0"

      [tool.aws-glue-toolkit]
      glue_version = "99.0"
      source = "missing"
      script = "missing.py"
      """
    When I run gtk-check-build on the file
    Then the hook should exit with failure
    And no temporary build files should remain in the project directory

  Scenario: Ignore projects that are not AWS Glue jobs
    Given a pyproject.toml file with content:
      """toml
      [project]
      name = "standard-python-pkg"
      version = "1.0.0"

      [tool.ruff]
      line-length = 79
      """
    When I run gtk-check-build on the file
    Then the hook should exit with success

  Scenario: Ignore pyproject.toml with malformed TOML content
    Given a pyproject.toml file with content:
      """toml
      [project
      invalid = toml syntax
      """
    When I run gtk-check-build on the file
    Then the hook should exit with success

  Scenario: Forward additional CLI arguments to build
    Given aws-glue-toolkit builds jobs successfully
    And a pyproject.toml file with content:
      """toml
      [project]
      name = "my-glue-job"

      [tool.aws-glue-toolkit]
      glue_version = "5.1"
      source = "src"
      script = "__main__.py"
      """
    When I run gtk-check-build with arguments "--mode host" on the file
    Then the hook should exit with success
    And the build command should include argument "--mode"
    And the build command should include argument "host"

  Scenario: Forward CLI arguments separated by double-dash delimiter
    Given aws-glue-toolkit builds jobs successfully
    And a pyproject.toml file with content:
      """toml
      [project]
      name = "my-glue-job"

      [tool.aws-glue-toolkit]
      glue_version = "5.1"
      source = "src"
      script = "__main__.py"
      """
    When I run gtk-check-build with arguments "--mode host --" on the file
    Then the hook should exit with success
    And the build command should include argument "--mode"
    And the build command should include argument "host"


  Scenario: Monorepo with mixed GTK and non-GTK projects
    Given aws-glue-toolkit builds jobs successfully
    And a workspace with projects:
      | directory   | is_gtk |
      | jobs/my-job | yes    |
      | libs/common | no     |
    When I run gtk-check-build on all project files
    Then the hook should exit with success

  Scenario: Monorepo with a failing GTK project
    Given aws-glue-toolkit fails to build job "jobs/broken-job"
    And a workspace with projects:
      | directory       | is_gtk |
      | jobs/good-job   | yes    |
      | jobs/broken-job | yes    |
    When I run gtk-check-build on all project files
    Then the hook should exit with failure

  Scenario: Run with no filenames provided
    When I run gtk-check-build with no arguments
    Then the hook should exit with success

  Scenario: Run on non-existent files
    When I run gtk-check-build on a non-existent file
    Then the hook should exit with success

  Scenario: Fail when aws-glue-toolkit is not installed
    Given aws-glue-toolkit is not installed
    And a pyproject.toml file with content:
      """toml
      [project]
      name = "my-glue-job"

      [tool.aws-glue-toolkit]
      glue_version = "5.1"
      source = "src"
      script = "__main__.py"
      """
    When I run gtk-check-build on the file
    Then the hook should exit with failure
    And stderr should mention "additional_dependencies"
