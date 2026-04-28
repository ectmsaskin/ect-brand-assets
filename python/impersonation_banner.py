"""ECT brand-assets v1.5.0 — impersonation banner, Python edition.

Mirrors templates/impersonation-banner.html.j2 for codebases that render
HTML without Jinja (e.g. ect-qa's f-string layer). Both must be updated
together; tests/test_lockup_parity.py enforces equivalence.
"""
from html import escape


def render_impersonation_banner(
    impersonated_by: str,
    current_user_email: str = '',
    asgard_admin_url: str = 'https://asgard.eastcoasttowing.com/admin/users',
) -> str:
    """Render the impersonation banner, or empty string if not impersonating.

    Args:
        impersonated_by: value of the X-Impersonated-By header (the
            super-admin's email). Empty string means no impersonation.
        current_user_email: the impersonated target (for display).
        asgard_admin_url: where the "Stop in Asgard" link points.
    """
    if not impersonated_by:
        return ''
    return (
        f'<div class="ect-impersonation-banner" role="alert">'
        f'<span> '
        f'Viewing as <strong>{escape(current_user_email)}</strong> '
        f'on behalf of <strong>{escape(impersonated_by)}</strong>. '
        f'</span>'
        f'<a href="{escape(asgard_admin_url)}" class="ect-impersonation-banner__link">Stop in Asgard</a>'
        f'</div>'
    )
