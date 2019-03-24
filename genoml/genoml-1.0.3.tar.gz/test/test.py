#! /usr/bin/env python -u
# coding=utf-8
import os
import shutil
import subprocess

__author__ = 'Sayed Hadi Hashemi'

test_cases = {
    "prune": {
        "args": "--model-file={model_file} --geno-prefix={geno_prefix} --pheno-file={pheno_file}",
        "validate_args": "--model-file={model_file} --valid-dir={valid_dir} --valid-geno-prefix={valid_geno_prefix} "
                         "--valid-pheno-file={valid_pheno_file} "
    },
    "prsice1gwas": {
        "args": "--model-file={model_file} --geno-prefix={geno_prefix} --pheno-file={pheno_file} --gwas-file={"
                "gwas_file}",
        "validate_args": "--model-file={model_file} --valid-dir={valid_dir} --valid-geno-prefix={valid_geno_prefix} "
                         "--valid-pheno-file={valid_pheno_file} "
    },
    "prsice2gwasCovAddit": {
        "args": "--model-file={model_file} --geno-prefix={geno_prefix} --pheno-file={pheno_file} --gwas-file={"
                "gwas_file} --cov-file={cov_file} --addit-file={add_file}",
        "validate_args": "--model-file={model_file} --valid-dir={valid_dir} --valid-geno-prefix={valid_geno_prefix} "
                         "--valid-pheno-file={valid_pheno_file} --valid-cov-file={valid_cov_file} "
                         "--valid-addit-file={valid_addit_file} "
    },
    "sblup1gwasAdditHerit": {
        "args": "--model-file={model_file} --geno-prefix={geno_prefix} --pheno-file={pheno_file} --gwas-file={"
                "gwas_file} --addit-file={add_file} --herit=0.2 ",
        "validate_args": "--model-file={model_file} --valid-dir={valid_dir} --valid-geno-prefix={valid_geno_prefix} "
                         "--valid-pheno-file={valid_pheno_file} --valid-addit-file={valid_addit_file} "
    }
}

files_to_check = [
    "_confMat.txt",
    "_confMatAtBestThresh_training.txt",
    "_tuned_confMat.txt",
    ".PRS_summary.txt",
    ".training_summary.txt",
    "_validation.validation_summary.txt",
    "_validation_validation_confMat.txt",
    "_validation_confMatAtBestThresh_validation.txt",
]
def test():
    for name, tc in test_cases.items():
        base_dir = f"test_results/{name}/"
        print(f"# {name}\necho ::: {name}")
        # print(f"mkdir -p {base_dir}")
        # print(f"cp -r ../example {base_dir}/")

        opts = {
            "model_file": os.path.join(base_dir, "model.genoml"),
            "valid_dir": os.path.join(base_dir, "valid"),

            "geno_prefix": os.path.join(base_dir, "example/training"),
            "pheno_file": os.path.join(base_dir, "example/training.pheno"),

            "gwas_file": os.path.join(base_dir, "example/example_GWAS.txt"),
            "cov_file": os.path.join(base_dir, "example/training.cov"),
            "add_file": os.path.join(base_dir, "example/training.addit"),

            "valid_geno_prefix": os.path.join(base_dir, "example/validation"),
            "valid_pheno_file": os.path.join(base_dir, "example/validation.pheno"),

            "valid_cov_file": os.path.join(base_dir, "example/validation.cov"),
            "valid_addit_file": os.path.join(base_dir, "example/validation.addit")
        }

        args = tc["args"].format(**opts) + " --n-cores=16"
        validate_args = tc["validate_args"].format(**opts) + " --n-cores=16"

        # print(f"genoml-train {args}")
        # print(f"genoml-inference {validate_args}")
        # print(f"tar -xf {opts['model_file']} -C {opts['valid_dir']}")

        ground_truth_dir = os.path.join("ground_truth", name, "model")
        result_dir = os.path.join(opts["valid_dir"], "model")
        for filename in files_to_check:
            print(f'diff -q {result_dir + filename} {ground_truth_dir + filename}')
        print()


if __name__ == "__main__":
    test()
