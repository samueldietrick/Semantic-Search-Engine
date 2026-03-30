"""Gera data/sample.json com 55+ itens variados."""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "sample.json"

random.seed(42)

cursos = [
    ("Curso de Laravel", "Aprenda Laravel do zero com projetos reais", "backend", "João Silva"),
    ("Python para Data Science", "Pandas, NumPy e visualização", "data", "Maria"),
    ("React Avançado", "Hooks, performance e testes", "frontend", "Carlos"),
    ("DevOps com Docker", "Containers e CI/CD", "devops", "Ana"),
    ("Segurança em APIs", "OAuth2, JWT e boas práticas", "seguranca", "Pedro"),
]

produtos = [
    ("Teclado mecânico", "Switch linear, RGB, layout ABNT2", "perifericos"),
    ("Monitor 27 4K", "IPS, 60Hz, calibração de cor", "monitores"),
    ("Webcam Full HD", "Autofoco, microfone duplo", "perifericos"),
    ("SSD NVMe 1TB", "Leitura 3500MB/s", "armazenamento"),
    ("Headset sem fio", "Cancelamento de ruído", "audio"),
]

artigos = [
    ("Autenticação em sistemas distribuídos", "Padrões de sessão e tokens stateless"),
    ("Observabilidade com OpenTelemetry", "Traces, métricas e logs correlacionados"),
    ("Testes de carga com k6", "Scripts e métricas úteis"),
    ("GraphQL vs REST", "Quando usar cada abordagem"),
]

usuarios = [
    ("Ana Backend", "10 anos em Java e microsserviços", ["java", "backend", "kafka"]),
    ("Bruno Frontend", "Especialista em React e acessibilidade", ["react", "frontend", "a11y"]),
    ("Carla Data", "ML e pipelines em Spark", ["python", "spark", "ml"]),
    ("Diego Mobile", "Kotlin e Swift em apps bancários", ["kotlin", "swift", "mobile"]),
]


def mk_item(i: int, extra: dict) -> dict:
    return {
        "id": f"item:{i}",
        "titulo": extra["titulo"],
        "descricao": extra["descricao"],
        "tags": extra["tags"],
        "metadata": extra["metadata"],
    }


def main() -> None:
    items: list[dict] = []
    n = 0

    for titulo, desc, cat, autor in cursos:
        n += 1
        items.append(
            mk_item(
                n,
                {
                    "titulo": titulo,
                    "descricao": desc,
                    "tags": ["curso", cat, "educacao"],
                    "metadata": {"categoria": "curso", "autor": autor, "preco": random.choice(["baixo", "medio"])},
                },
            )
        )

    for titulo, desc, cat in produtos:
        n += 1
        items.append(
            mk_item(
                n,
                {
                    "titulo": titulo,
                    "descricao": desc,
                    "tags": ["produto", cat, "hardware"],
                    "metadata": {
                        "categoria": "produto",
                        "avaliacao": round(random.uniform(3.5, 5.0), 1),
                        "preco": random.choice(["barato", "medio", "alto"]),
                    },
                },
            )
        )

    for titulo, desc in artigos:
        n += 1
        items.append(
            mk_item(
                n,
                {
                    "titulo": titulo,
                    "descricao": desc,
                    "tags": ["artigo", "tecnologia", "engenharia"],
                    "metadata": {"categoria": "artigo", "tipo": "blog"},
                },
            )
        )

    for nome, bio, tags in usuarios:
        n += 1
        items.append(
            mk_item(
                n,
                {
                    "titulo": nome,
                    "descricao": bio,
                    "tags": tags + ["perfil"],
                    "metadata": {"categoria": "usuario", "experiencia_anos": random.randint(3, 15)},
                },
            )
        )

    # Itens adicionais variados
    extras = [
        ("Notebook gamer", "RTX, 16GB RAM, tela 144Hz", ["notebook", "gamer"], {"categoria": "produto", "preco": "alto"}),
        ("Curso de Go", "Concorrência e APIs em Go", ["go", "backend", "curso"], {"categoria": "curso", "autor": "Luiz"}),
        ("Vue 3 Composition API", "Guia prático com Pinia", ["vue", "frontend"], {"categoria": "curso"}),
        ("PostgreSQL avançado", "Índices, locks e replicação", ["sql", "dba"], {"categoria": "curso"}),
        ("Artigo: OAuth2", "Fluxos authorization code e PKCE", ["oauth", "seguranca"], {"categoria": "artigo"}),
        ("Usuário: SRE", "Experiência em Kubernetes e SLOs", ["sre", "kubernetes", "observabilidade"], {"categoria": "usuario"}),
        ("Mouse ergonômico", "Reduz tensão no punho", ["mouse", "ergonomia"], {"categoria": "produto", "preco": "medio"}),
        ("Curso de Rust", "Ownership sem medo", ["rust", "systems"], {"categoria": "curso"}),
        ("Artigo: WebSockets", "Escalabilidade e heartbeats", ["websocket", "realtime"], {"categoria": "artigo"}),
        ("Usuário: QA", "Automação com Playwright", ["qa", "testes", "playwright"], {"categoria": "usuario"}),
        ("Tablet Android", "Stylus, ideal para leitura", ["tablet", "android"], {"categoria": "produto"}),
        ("Curso de TypeScript", "Tipos avançados e generics", ["typescript", "frontend"], {"categoria": "curso"}),
        ("Artigo: CQRS", "Separar leitura e escrita", ["cqrs", "arquitetura"], {"categoria": "artigo"}),
        ("Usuário: Data Eng", "Airflow e dbt em produção", ["airflow", "dbt", "data"], {"categoria": "usuario"}),
        ("Hub USB-C", "7 portas, alimentação", ["hub", "usb"], {"categoria": "produto", "preco": "barato"}),
        ("Curso de Elasticsearch", "Busca textual e agregações", ["elasticsearch", "busca"], {"categoria": "curso"}),
        ("Artigo: Feature flags", "Deploy gradual e experimentos", ["feature-flags", "release"], {"categoria": "artigo"}),
        ("Usuário: Mobile", "Flutter em apps de saúde", ["flutter", "dart", "mobile"], {"categoria": "usuario"}),
        ("Cadeira escritório", "Lombar ajustável", ["moveis", "escritorio"], {"categoria": "produto"}),
        ("Curso de GraphQL", "Schema, resolvers e federation", ["graphql", "api"], {"categoria": "curso"}),
        ("Artigo: Zero trust", "Identidade em redes corporativas", ["zero-trust", "seguranca"], {"categoria": "artigo"}),
        ("Usuário: Backend", "Node.js e event-driven em escala", ["nodejs", "backend", "eventos"], {"categoria": "usuario"}),
        ("Microfone condensador", "Gravação de podcast", ["audio", "podcast"], {"categoria": "produto"}),
        ("Curso de Kubernetes", "Deployments, services e ingress", ["kubernetes", "devops"], {"categoria": "curso"}),
        ("Artigo: Idempotência", "Chaves e deduplicação", ["api", "rest"], {"categoria": "artigo"}),
        ("Usuário: Frontend", "Design systems e Storybook", ["design-system", "frontend"], {"categoria": "usuario"}),
        ("Roteador Wi-Fi 6", "Mesh e baixa latência", ["rede", "wifi"], {"categoria": "produto"}),
        ("Curso de SQL", "Consultas analíticas e otimização", ["sql", "dados"], {"categoria": "curso"}),
        ("Artigo: LGPD", "Bases legais e DPIA", ["lgpd", "privacidade"], {"categoria": "artigo"}),
        ("Usuário: Segurança", "Pentest e hardening de cloud", ["seguranca", "cloud"], {"categoria": "usuario"}),
        ("Curso de UX Research", "Entrevistas e jornadas do usuário", ["ux", "pesquisa"], {"categoria": "curso"}),
        ("Produto barato com boa avaliação", "Fone intra-auricular básico bem avaliado", ["audio", "custo-beneficio"], {"categoria": "produto", "preco": "barato", "avaliacao": 4.8}),
        ("Documentos sobre autenticação", "Coleção de guias SAML e OIDC", ["autenticacao", "documentacao"], {"categoria": "artigo"}),
        ("Pessoa backend sênior", "Arquitetura de APIs e mensageria", ["backend", "senior", "api"], {"categoria": "usuario"}),
    ]

    for titulo, desc, tags, meta in extras:
        n += 1
        items.append(
            mk_item(
                n,
                {
                    "titulo": titulo,
                    "descricao": desc,
                    "tags": tags,
                    "metadata": meta,
                },
            )
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Escrito {len(items)} itens em {OUT}")


if __name__ == "__main__":
    main()
