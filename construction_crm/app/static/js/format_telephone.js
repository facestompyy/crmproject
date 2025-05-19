// Format (xxx)xxx-xxxx automatically
document.getElementById('telephone')?.addEventListener('input', function(e) {
    let nums = e.target.value.replace(/\D/g, '');
    let formatted = nums.length > 0 ? '(' + nums.substring(0,3) : '';
    formatted += nums.length > 3 ? ')' + nums.substring(3,6) : '';
    formatted += nums.length > 6 ? '-' + nums.substring(6,10) : '';
    e.target.value = formatted.substring(0, 14);
});