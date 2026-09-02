"""Dataset validation suite for DCAT.

Performs strict integrity checks on normalized dataset records:
- Schema & field validation
- Label sanity (0=ham, 1=spam)
- Modality consistency against content flags
- Duplicate email ID detection
- Image reference & filter consistency checks
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from dcat.data.modalities import modality_from_flags
from dcat.data.records import EmailRecord


@dataclass
class ValidationIssue:
    """A single validation warning or error."""

    severity: str  # "ERROR" or "WARNING"
    email_id: str
    code: str
    message: str


@dataclass
class ValidationReport:
    """Summary report of dataset validation."""

    total_records: int
    error_count: int
    warning_count: int
    passed: bool
    issues: list[ValidationIssue]

    def to_dict(self) -> dict:
        return {
            "total_records": self.total_records,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "passed": self.passed,
            "issues": [asdict(issue) for issue in self.issues],
        }

    def render_text(self) -> str:
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("DCAT Dataset Validation Report")
        lines.append("=" * 60)
        lines.append(f"Total Records Analyzed : {self.total_records}")
        lines.append(f"Errors Found           : {self.error_count}")
        lines.append(f"Warnings Found         : {self.warning_count}")
        lines.append(f"Validation Status      : {'PASS' if self.passed else 'FAIL'}")
        lines.append("-" * 60)
        for issue in self.issues[:50]:  # Cap CLI output at 50 issues
            lines.append(f"[{issue.severity:<7}] {issue.email_id}: {issue.code} - {issue.message}")
        if len(self.issues) > 50:
            lines.append(f"... and {len(self.issues) - 50} more issues.")
        lines.append("=" * 60)
        return "\n".join(lines)


class DatasetValidator:
    """Strict dataset validator for EmailRecord datasets."""

    def validate(self, records: Sequence[EmailRecord]) -> ValidationReport:
        issues: list[ValidationIssue] = []
        seen_ids: set[str] = set()

        for rec in records:
            # 1. Duplicate ID check
            if rec.email_id in seen_ids:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        email_id=rec.email_id,
                        code="duplicate_email_id",
                        message=f"Duplicate email ID observed: {rec.email_id}",
                    )
                )
            seen_ids.add(rec.email_id)

            # 2. Label validity
            if rec.label is not None and rec.label not in (0, 1):
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        email_id=rec.email_id,
                        code="invalid_label",
                        message=f"Invalid label {rec.label!r}; expected 0, 1, or None",
                    )
                )

            # 3. Modality consistency
            expected_modality = modality_from_flags(rec.has_text, rec.has_meaningful_image)
            if rec.modality != expected_modality:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        email_id=rec.email_id,
                        code="inconsistent_modality",
                        message=f"Modality {rec.modality.value!r} does not match flags (has_text={rec.has_text}, has_image={rec.has_meaningful_image})",
                    )
                )

            # 4. Text flag consistency
            if rec.has_text and not (rec.text and rec.text.strip()):
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        email_id=rec.email_id,
                        code="empty_text_flagged",
                        message="has_text is True but text body is empty or whitespace",
                    )
                )

            # 5. Image record consistency
            meaningful_count = sum(1 for img in rec.images if not img.filtered)
            if rec.has_meaningful_image and meaningful_count == 0:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        email_id=rec.email_id,
                        code="missing_meaningful_image",
                        message="has_meaningful_image is True but zero non-filtered images exist",
                    )
                )

            for img in rec.images:
                if img.filtered and not img.filter_reason:
                    issues.append(
                        ValidationIssue(
                            severity="ERROR",
                            email_id=rec.email_id,
                            code="missing_filter_reason",
                            message=f"Image {img.image_id} is filtered but has no filter_reason",
                        )
                    )

            # 6. Split assignment check (warning)
            if rec.split and rec.split not in ("train", "val", "test"):
                issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        email_id=rec.email_id,
                        code="unknown_split",
                        message=f"Non-standard split assignment: {rec.split!r}",
                    )
                )

        error_count = sum(1 for i in issues if i.severity == "ERROR")
        warning_count = sum(1 for i in issues if i.severity == "WARNING")
        passed = error_count == 0

        return ValidationReport(
            total_records=len(records),
            error_count=error_count,
            warning_count=warning_count,
            passed=passed,
            issues=issues,
        )


__all__ = ["DatasetValidator", "ValidationIssue", "ValidationReport"]
