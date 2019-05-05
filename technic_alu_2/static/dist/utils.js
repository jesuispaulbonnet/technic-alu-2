
export function get_base_url() {
    let current_href = window.location.href;
    let current_path = window.location.pathname;
    return current_href.replace(current_path, '');
}
