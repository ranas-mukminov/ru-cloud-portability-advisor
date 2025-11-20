provider "hcloud" {
  token = "DUMMY"
}

resource "hcloud_server" "node" {
  name        = "demo"
  server_type = "cx11"
  image       = "ubuntu-22.04"
}

resource "hcloud_load_balancer" "lb" {
  name = "lb-demo"
  type = "lb11"
}

resource "hcloud_volume" "data" {
  name   = "data"
  size   = 10
  server_id = hcloud_server.node.id
}

