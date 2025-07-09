# Diagrama de Deployment

## Arquitetura de Infraestrutura

```mermaid
graph TB
    subgraph "Docker Compose"
        subgraph "Container: avantsoft-app"
            Django[Django App]
            DRF[Django REST Framework]
            JWT[JWT Authentication]
            Spectacular[drf-spectacular]
        end
        
        subgraph "Container: avantsoft-db"
            PostgreSQL[(PostgreSQL)]
        end
        
        subgraph "Container: avantsoft-pgadmin"
            pgAdmin[pgAdmin]
        end
    end
    
    subgraph "Host Machine"
        Docker[Docker Engine]
        Volumes[Volumes]
        Network[Docker Network]
    end
    
    subgraph "External"
        Client[API Client]
        Browser[Web Browser]
    end
    
    Client -->|HTTP/8000| Django
    Browser -->|HTTP/8000| Django
    Browser -->|HTTP/5050| pgAdmin
    
    Django -->|SQL| PostgreSQL
    pgAdmin -->|SQL| PostgreSQL
    
    Django --> Volumes
    PostgreSQL --> Volumes
    
    Django --> Network
    PostgreSQL --> Network
    pgAdmin --> Network
```

## Estrutura de Containers

```mermaid
graph LR
    subgraph "Docker Compose Services"
        App[app:8000]
        DB[db:5432]
        PgAdmin[pgadmin:5050]
    end
    
    subgraph "Dependencies"
        Poetry[Poetry]
        Python[Python 3.11]
        Gunicorn[Gunicorn]
    end
    
    subgraph "Technologies"
        Django[Django 5.2]
        DRF[DRF]
        JWT[JWT]
        Spectacular[Spectacular]
    end
    
    App --> Poetry
    Poetry --> Python
    Python --> Gunicorn
    Gunicorn --> Django
    Django --> DRF
    Django --> JWT
    Django --> Spectacular
```

## Configuração de Rede

```mermaid
graph TB
    subgraph "Docker Network: avantsoft_default"
        App[avantsoft-app:8000]
        DB[avantsoft-db:5432]
        PgAdmin[avantsoft-pgadmin:5050]
    end
    
    subgraph "Port Mappings"
        Host8000[localhost:8000]
        Host5432[localhost:5432]
        Host5050[localhost:5050]
    end
    
    Host8000 --> App
    Host5432 --> DB
    Host5050 --> PgAdmin
```

## Volumes e Persistência

```mermaid
graph LR
    subgraph "Host Volumes"
        AppLogs[./app.log]
        PostgresData[./postgres_data]
        PgAdminData[./pgadmin_data]
    end
    
    subgraph "Container Volumes"
        AppVolume[/app]
        DBVolume[/var/lib/postgresql/data]
        PgAdminVolume[/var/lib/pgadmin]
    end
    
    AppLogs --> AppVolume
    PostgresData --> DBVolume
    PgAdminData --> PgAdminVolume
```

## Variáveis de Ambiente

```mermaid
graph TB
    subgraph ".env File"
        DEBUG[DEBUG=1]
        SECRET_KEY[SECRET_KEY=changeme]
        DB_NAME[DB_NAME=loja_brinquedos]
        DB_USER[DB_USER=postgres]
        DB_PASSWORD[DB_PASSWORD=postgres]
        DB_HOST[DB_HOST=db]
        DB_PORT[DB_PORT=5432]
    end
    
    subgraph "Django Settings"
        Settings[settings.py]
        Database[DATABASES]
        Logging[LOGGING]
        REST_FRAMEWORK[REST_FRAMEWORK]
    end
    
    DEBUG --> Settings
    SECRET_KEY --> Settings
    DB_NAME --> Database
    DB_USER --> Database
    DB_PASSWORD --> Database
    DB_HOST --> Database
    DB_PORT --> Database
```

## Fluxo de Deployment

```mermaid
sequenceDiagram
    participant Dev
    participant Docker
    participant App
    participant DB
    participant PgAdmin
    
    Dev->>Docker: docker-compose build
    Docker->>App: Build image
    Docker->>DB: Pull PostgreSQL
    Docker->>PgAdmin: Pull pgAdmin
    
    Dev->>Docker: docker-compose up -d
    Docker->>DB: Start PostgreSQL
    Docker->>PgAdmin: Start pgAdmin
    Docker->>App: Start Django
    
    App->>DB: Wait for connection
    DB-->>App: Connection established
    
    App->>App: Run migrations
    App->>App: Collect static
    App-->>Dev: Ready on :8000
```

## Monitoramento e Logs

```mermaid
graph TB
    subgraph "Logging"
        AppLogs[Application Logs]
        DBLogs[Database Logs]
        AccessLogs[Access Logs]
    end
    
    subgraph "Monitoring"
        HealthCheck[Health Checks]
        Metrics[Metrics]
        Errors[Error Tracking]
    end
    
    subgraph "Files"
        app_log[app.log]
        django_log[Django logs]
        gunicorn_log[Gunicorn logs]
    end
    
    AppLogs --> app_log
    DBLogs --> django_log
    AccessLogs --> gunicorn_log
    
    HealthCheck --> Metrics
    Metrics --> Errors
```

## Segurança

```mermaid
graph TB
    subgraph "Authentication"
        JWT[JWT Tokens]
        Bearer[Bearer Authentication]
        Refresh[Token Refresh]
    end
    
    subgraph "Authorization"
        IsAuthenticated[IsAuthenticated]
        Permissions[Custom Permissions]
    end
    
    subgraph "Data Protection"
        HTTPS[HTTPS (Production)]
        CORS[CORS Headers]
        CSRF[CSRF Protection]
    end
    
    JWT --> Bearer
    Bearer --> IsAuthenticated
    IsAuthenticated --> Permissions
    
    HTTPS --> CORS
    CORS --> CSRF
```

## Escalabilidade

```mermaid
graph LR
    subgraph "Current Setup"
        SingleApp[Single Django App]
        SingleDB[Single PostgreSQL]
    end
    
    subgraph "Scalable Setup"
        MultipleApps[Multiple Django Apps]
        LoadBalancer[Load Balancer]
        ReadReplicas[Read Replicas]
        Cache[Redis Cache]
    end
    
    SingleApp --> MultipleApps
    SingleDB --> ReadReplicas
    MultipleApps --> LoadBalancer
    LoadBalancer --> Cache
``` 