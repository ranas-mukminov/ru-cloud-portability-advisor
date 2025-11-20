from enum import Enum, auto


class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    HETZNER = "hetzner"
    YANDEX = "yandex"
    VK = "vk"
    CLOUD_RU = "cloud_ru"
    SELECTEL = "selectel"
    UNKNOWN = "unknown"


class ServiceKind(str, Enum):
    STORAGE = "storage"
    DATABASE = "database"
    COMPUTE = "compute"
    KUBERNETES = "kubernetes"
    LOAD_BALANCER = "load_balancer"
    QUEUE = "queue"
    FUNCTION = "function"
    NETWORK = "network"
    K8S_OBJECT = "k8s_object"


class MigrationStatus(str, Enum):
    DIRECT = "direct"
    NEEDS_REFACTOR = "needs_refactor"
    NO_ANALOG = "no_analog"

