provider "google" {
  region = "europe-west1"
}

resource "google_storage_bucket" "sample" {
  name          = "sample-gcs-bucket"
  location      = "EU"
  force_destroy = true
}

resource "google_sql_database_instance" "db" {
  name             = "sample-sql"
  database_version = "POSTGRES_13"
  region           = "europe-west1"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_container_cluster" "gke" {
  name     = "gke-sample"
  location = "europe-west1-b"
}

resource "google_cloudfunctions_function" "fn" {
  name        = "http-fn"
  runtime     = "nodejs18"
  entry_point = "hello"
  source_archive_bucket = google_storage_bucket.sample.name
  source_archive_object = "source.zip"
}

