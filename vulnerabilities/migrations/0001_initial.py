# Generated by Django 3.0.7 on 2021-02-18 06:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Importer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the importer", max_length=100, unique=True),
                ),
                (
                    "license",
                    models.CharField(
                        blank=True, help_text="License of the vulnerability data", max_length=100
                    ),
                ),
                (
                    "last_run",
                    models.DateTimeField(help_text="UTC Timestamp of the last run", null=True),
                ),
                (
                    "data_source",
                    models.CharField(
                        help_text="Name of the data source implementation importable from vulnerabilities.importers",
                        max_length=100,
                    ),
                ),
                (
                    "data_source_cfg",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        default=dict,
                        help_text="Implementation-specific configuration for the data source",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ImportProblem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("conflicting_model", django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        help_text="A short code to identify the type of this package. For example: gem for a Rubygem, docker for a container, pypi for a Python Wheel or Egg, maven for a Maven Jar, deb for a Debian package, etc.",
                        max_length=16,
                    ),
                ),
                (
                    "namespace",
                    models.CharField(
                        blank=True,
                        help_text="Package name prefix, such as Maven groupid, Docker image owner, GitHub user or organization, etc.",
                        max_length=255,
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, help_text="Name of the package.", max_length=100),
                ),
                (
                    "version",
                    models.CharField(
                        blank=True, help_text="Version of the package.", max_length=100
                    ),
                ),
                (
                    "subpath",
                    models.CharField(
                        blank=True,
                        help_text="Extra subpath within a package, relative to the package root.",
                        max_length=200,
                    ),
                ),
                (
                    "qualifiers",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        default=dict,
                        help_text="Extra qualifying data for a package such as the name of an OS, architecture, distro, etc.",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vulnerability",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "vulnerability_id",
                    models.CharField(
                        help_text="Unique vulnerability_id for a vulnerability: this is either a published CVE id (as in CVE-2020-7965) if it exists. Otherwise this is a VulnerableCode-assigned VULCOID (as in VULCOID-2021-01-23-15-12). When a vulnerability CVE is assigned later we replace this with the CVE and keep the 'old' VULCOID in the 'old_vulnerability_id' field to support redirection to the CVE id.",
                        max_length=50,
                        unique=True,
                    ),
                ),
                (
                    "old_vulnerability_id",
                    models.CharField(
                        help_text="empty if no  CVE else VC id",
                        max_length=50,
                        null=True,
                        unique=True,
                    ),
                ),
                ("summary", models.TextField(blank=True, help_text="Summary of the vulnerability")),
            ],
            options={
                "verbose_name_plural": "Vulnerabilities",
            },
        ),
        migrations.CreateModel(
            name="VulnerabilityReference",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "source",
                    models.CharField(blank=True, help_text="Source(s) name eg:NVD", max_length=50),
                ),
                (
                    "reference_id",
                    models.CharField(
                        blank=True, help_text="Reference ID, eg:DSA-4465-1", max_length=50
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, help_text="URL of Vulnerability data", max_length=1024
                    ),
                ),
                (
                    "vulnerability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vulnerabilities.Vulnerability",
                    ),
                ),
            ],
            options={
                "unique_together": {("vulnerability", "source", "reference_id", "url")},
            },
        ),
        migrations.CreateModel(
            name="PackageRelatedVulnerability",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("is_vulnerable", models.BooleanField()),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vulnerabilities.Package"
                    ),
                ),
                (
                    "vulnerability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vulnerabilities.Vulnerability",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "PackageRelatedVulnerabilities",
                "unique_together": {("package", "vulnerability")},
            },
        ),
        migrations.AddField(
            model_name="package",
            name="vulnerabilities",
            field=models.ManyToManyField(
                through="vulnerabilities.PackageRelatedVulnerability",
                to="vulnerabilities.Vulnerability",
            ),
        ),
        migrations.CreateModel(
            name="VulnerabilitySeverity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "value",
                    models.CharField(help_text="Example: 9.0, Important, High", max_length=50),
                ),
                (
                    "scoring_system",
                    models.CharField(
                        choices=[
                            ("cvssv2", "CVSSv2 Base Score"),
                            ("cvssv2_vector", "CVSSv2 Vector"),
                            ("cvssv3", "CVSSv3 Base Score"),
                            ("cvssv3_vector", "CVSSv3 Vector"),
                            ("cvssv3.1", "CVSSv3.1 Base Score"),
                            ("cvssv3.1_vector", "CVSSv3.1 Vector"),
                            ("rhbs", "RedHat Bugzilla severity"),
                            ("rhas", "RedHat Aggregate severity"),
                            ("avgs", "Archlinux Vulnerability Group Severity"),
                        ],
                        help_text="vulnerability_id for the scoring system used. Available choices are: cvssv2 is vulnerability_id for CVSSv2 Base Score system, cvssv2_vector is vulnerability_id for CVSSv2 Vector system, cvssv3 is vulnerability_id for CVSSv3 Base Score system, cvssv3_vector is vulnerability_id for CVSSv3 Vector system, cvssv3.1 is vulnerability_id for CVSSv3.1 Base Score system, cvssv3.1_vector is vulnerability_id for CVSSv3.1 Vector system, rhbs is vulnerability_id for RedHat Bugzilla severity system, rhas is vulnerability_id for RedHat Aggregate severity system, avgs is vulnerability_id for Archlinux Vulnerability Group Severity system ",
                        max_length=50,
                    ),
                ),
                (
                    "reference",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vulnerabilities.VulnerabilityReference",
                    ),
                ),
                (
                    "vulnerability",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vulnerabilities.Vulnerability",
                    ),
                ),
            ],
            options={
                "unique_together": {("vulnerability", "reference", "scoring_system")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="package",
            unique_together={("name", "namespace", "type", "version", "qualifiers", "subpath")},
        ),
    ]
