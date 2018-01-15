function getValueOrNull(value) {
    if (value.trim()) {
        return value.trim();
    }
    return null;
}

function isNotEmpty(value) {
    if (value.trim()) {
        return true;
    }

    return false;
}