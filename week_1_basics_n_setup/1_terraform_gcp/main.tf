terraform {
  required_version = "1.5.7"
  required_providers {
    google = {
        source  = "hashicorp/google"
        version = "4.82.0" # https://github.com/hashicorp/terraform-provider-google-beta/releases
    }
  }
}

provider "google" {
    project = "evocative-tide-398716"
    region  = "us-east4" # N. Virginia
    zone    = "us-east4-a" # See regions and zones at https://cloud.google.com/compute/docs/regions-zones
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "data-lake-bucket"
  location      = "us-east4"
  storage_class = "STANDARD"
  force_destroy = true
  versioning {
    enabled = true
  }
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}
