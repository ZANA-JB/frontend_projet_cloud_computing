// shared helper functions used across pages
function iconName(type) {
    switch(type){
        case 'pdf': return 'picture_as_pdf';
        case 'image': return 'image';
        case 'video': return 'movie';
        case 'archive': return 'inventory_2';
        case 'doc': return 'description';
        case 'sheet': return 'table_view';
        case 'code': return 'code';
        default: return 'insert_drive_file';
    }
}
function iconBgColor(type){
    switch(type){
        case 'pdf': return 'bg-red-50 dark:bg-red-900/20';
        case 'image': return 'bg-blue-50 dark:bg-blue-900/20';
        case 'video': return 'bg-purple-50 dark:bg-purple-900/20';
        case 'archive': return 'bg-amber-50 dark:bg-amber-900/20';
        case 'doc': return 'bg-blue-50 dark:bg-blue-900/20';
        case 'sheet': return 'bg-emerald-50 dark:bg-emerald-900/20';
        case 'code': return 'bg-slate-100 dark:bg-slate-700';
        default: return 'bg-slate-50 dark:bg-slate-700/20';
    }
}
function iconColor(type){
    switch(type){
        case 'pdf': return 'red-600 dark:text-red-400';
        case 'image': return 'blue-600 dark:text-blue-400';
        case 'video': return 'purple-600 dark:text-purple-400';
        case 'archive': return 'amber-600 dark:text-amber-400';
        case 'doc': return 'blue-700 dark:text-blue-300';
        case 'sheet': return 'emerald-600 dark:text-emerald-400';
        case 'code': return 'slate-600 dark:text-slate-300';
        default: return 'slate-600 dark:text-slate-300';
    }
}

// simple global utility to guard protected routes in front end (optional)
function ensureLoggedIn() {
    // could check a cookie or call /api/me; placeholder
}

// export to window to make available in inline scripts
window.iconName = iconName;
window.iconBgColor = iconBgColor;
window.iconColor = iconColor;

// auto-fill upload name from filename if user hasn't typed anything
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const nameInput = document.querySelector('input[name="name"]');
    if (fileInput && nameInput) {
        fileInput.addEventListener('change', () => {
            const file = fileInput.files[0];
            if (file && !nameInput.value.trim()) {
                const base = file.name.replace(/\.[^/.]+$/, '');
                nameInput.value = base;
            }
        });
    }

    // debug form submission for upload (guided by the new backend instructions)
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            console.log('=== DEBUT UPLOAD ===');
            const fileInput = document.getElementById('file-input');
            const file = fileInput.files[0];
            const name = document.querySelector('input[name="name"]').value;
            const status = document.querySelector('input[name="status"]:checked')?.value;
            const userIdField = document.querySelector('input[name="user_id"]');
            const formUserId = userIdField ? userIdField.value : null;

            console.log('1. Fichier:', file);
            console.log('2. Nom:', name);
            console.log('3. User ID:', formUserId);
            console.log('4. Status:', status);

            if (!file) {
                console.error('❌ Pas de fichier');
                // allow form validation to catch it
            }

            if (file && file.size > 10 * 1024 * 1024) {
                alert('Fichier trop volumineux (max 10 MB)');
                e.preventDefault();
                return;
            }

            if (!formUserId) {
                console.error('❌ Pas d\'utilisateur connecté (user_id manquant)');
            }

            // dump all form data
            const data = new FormData(uploadForm);
            console.log('5. FormData créé');
            for (let [key, value] of data.entries()) {
                console.log(`   ${key}:`, value);
            }
            console.log('=== FIN DEBUG ===');
        });
    }
});
