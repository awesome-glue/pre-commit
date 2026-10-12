Feature: Sort dependencies in pyproject.toml
  As a developer maintaining AWS Glue jobs
  I want pre-commit to sort dependencies in pyproject.toml
  So that dependencies under [project] and [tool.aws-glue-toolkit] are consistently ordered

  Scenario: Sort unsorted dependencies under [project]
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = [
          "z-pkg",
          "a-pkg",
      ]
      """
    When I run gtk-sort-deps on the file
    Then the file should be updated to:
      """toml
      [project]
      dependencies = [
          "a-pkg",
          "z-pkg",
      ]
      """
    And the hook should exit with failure

  Scenario: Sort unsorted dependencies under [tool.aws-glue-toolkit]
    Given a pyproject.toml file with content:
      """toml
      [tool.aws-glue-toolkit]
      dependencies = [
          "boto3",
          "aws-glue-toolkit",
      ]
      """
    When I run gtk-sort-deps on the file
    Then the file should be updated to:
      """toml
      [tool.aws-glue-toolkit]
      dependencies = [
          "aws-glue-toolkit",
          "boto3",
      ]
      """
    And the hook should exit with failure

  Scenario: Sort dependencies in both [project] and [tool.aws-glue-toolkit]
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = ["z-pkg", "a-pkg"]

      [tool.aws-glue-toolkit]
      dependencies = ["y-pkg", "b-pkg"]
      """
    When I run gtk-sort-deps on the file
    Then the file should be updated to:
      """toml
      [project]
      dependencies = ["a-pkg", "z-pkg"]

      [tool.aws-glue-toolkit]
      dependencies = ["b-pkg", "y-pkg"]
      """
    And the hook should exit with failure

  Scenario: Sort dependencies case-insensitively
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = [
          "requests",
          "Boto3",
          "aws-glue-toolkit",
          "Pillow",
      ]
      """
    When I run gtk-sort-deps on the file
    Then the file should be updated to:
      """toml
      [project]
      dependencies = [
          "aws-glue-toolkit",
          "Boto3",
          "Pillow",
          "requests",
      ]
      """
    And the hook should exit with failure

  Scenario: Preserve comments and formatting during sorting
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = [
          "z-pkg>=1.0",  # comment for z
          "a-pkg",
      ]
      """
    When I run gtk-sort-deps on the file
    Then the file should be updated to:
      """toml
      [project]
      dependencies = [
          "a-pkg",
          "z-pkg>=1.0",  # comment for z
      ]
      """
    And the hook should exit with failure

  Scenario: Leave already sorted dependencies unchanged
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = [
          "a-pkg",
          "z-pkg",
      ]
      """
    When I run gtk-sort-deps on the file
    Then the file content should remain unchanged
    And the hook should exit with success

  Scenario: Leave empty or single item dependencies unchanged
    Given a pyproject.toml file with content:
      """toml
      [project]
      dependencies = ["single-pkg"]

      [tool.aws-glue-toolkit]
      dependencies = []
      """
    When I run gtk-sort-deps on the file
    Then the file content should remain unchanged
    And the hook should exit with success

  Scenario: Ignore pyproject.toml without dependency sections
    Given a pyproject.toml file with content:
      """toml
      [project]
      name = "my-job"
      version = "0.1.0"
      """
    When I run gtk-sort-deps on the file
    Then the file content should remain unchanged
    And the hook should exit with success

  Scenario: Run with no filenames provided
    When I run gtk-sort-deps with no arguments
    Then the hook should exit with success

  Scenario: Run on non-existent files
    When I run gtk-sort-deps on a non-existent file
    Then the hook should exit with success
