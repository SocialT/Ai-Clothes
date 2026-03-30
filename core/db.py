from prisma import Prisma
import os
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


def _ensure_pgbouncer_param(database_url: str) -> str:
    """Append pgbouncer=true to the DATABASE_URL if not present.

    This avoids Postgres 42P05 (prepared statement already exists) errors
    when connecting via PgBouncer/Supabase pooled connections by disabling
    prepared statements in Prisma's query engine.
    """
    if not database_url:
        return database_url

    parsed = urlparse(database_url)
    query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if "pgbouncer" not in query_params:
        query_params["pgbouncer"] = "true"
        new_query = urlencode(query_params)
        parsed = parsed._replace(query=new_query)
        return urlunparse(parsed)
    return database_url


_raw_url = os.getenv("DATABASE_URL", "")
_safe_url = _ensure_pgbouncer_param(_raw_url)

# Global database instance configured with safe URL
db = Prisma(datasource={"url": _safe_url} if _safe_url else None)
