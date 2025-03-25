// プロジェクト関連の表示切替
function toggleNewProjectForm() {
    const form = document.getElementById('new-project-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function toggleEditProjectForm() {
    const form = document.getElementById('edit-project-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function toggleDeleteProjectForm() {
    const form = document.getElementById('delete-project-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    // 新規プロジェクトボタン
    const newProjectBtn = document.getElementById('new-project-btn');
    if (newProjectBtn) {
        newProjectBtn.addEventListener('click', toggleNewProjectForm);
    }

    // プロジェクト編集ボタン
    const editProjectBtn = document.getElementById('edit-project-btn');
    if (editProjectBtn) {
        editProjectBtn.addEventListener('click', toggleEditProjectForm);
    }

    // プロジェクト削除ボタン
    const deleteProjectBtn = document.getElementById('delete-project-btn');
    if (deleteProjectBtn) {
        deleteProjectBtn.addEventListener('click', toggleDeleteProjectForm);
    }

    // アイテム編集ボタン
    const editItemBtns = document.querySelectorAll('.edit-item-btn');
    editItemBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const li = this.closest('li');
            const itemContent = li.querySelector('.item-content');
            const currentText = itemContent.textContent.trim();
            
            // 編集モードに切り替え
            li.classList.add('editing');
            
            // 編集フォームを作成
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentText;
            input.className = 'edit-input';
            
            // 保存・キャンセルボタンを作成
            const editActions = document.createElement('div');
            editActions.className = 'edit-actions';
            
            const saveBtn = document.createElement('button');
            saveBtn.textContent = '保存';
            saveBtn.className = 'btn';
            saveBtn.addEventListener('click', function() {
                saveItem(li);
            });
            
            const cancelBtn = document.createElement('button');
            cancelBtn.textContent = 'キャンセル';
            cancelBtn.className = 'btn cancel';
            cancelBtn.addEventListener('click', function() {
                cancelEdit(li, currentText);
            });
            
            editActions.appendChild(saveBtn);
            editActions.appendChild(cancelBtn);
            
            // 内容を編集フォームに置き換え
            itemContent.innerHTML = '';
            itemContent.appendChild(input);
            li.appendChild(editActions);
            
            // 入力フィールドにフォーカス
            input.focus();
            input.setSelectionRange(input.value.length, input.value.length);
        });
    });

    // アイテム削除ボタン
    const deleteItemBtns = document.querySelectorAll('.delete-item-btn');
    deleteItemBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const li = this.closest('li');
            const pointCard = li.closest('.point-card');
            const pointType = pointCard.dataset.pointType;
            const itemIndex = li.dataset.index;
            
            if (confirm('このアイテムを削除しますか？')) {
                deleteItem(pointType, itemIndex);
            }
        });
    });
});

// アイテム編集の保存
function saveItem(li) {
    const input = li.querySelector('.edit-input');
    const newText = input.value.trim();
    
    if (!newText) {
        alert('テキストを入力してください');
        return;
    }
    
    const pointCard = li.closest('.point-card');
    const pointType = pointCard.dataset.pointType;
    const itemIndex = li.dataset.index;
    
    // プロジェクトIDの取得（URLから抽出）
    const urlParts = window.location.pathname.split('/');
    const projectId = urlParts[urlParts.length - 1];
    
    // サーバーに編集内容を送信
    const formData = new FormData();
    formData.append('point_type', pointType);
    formData.append('item_index', itemIndex);
    formData.append('new_text', newText);
    
    fetch(`/project/${projectId}/item/update`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const itemContent = li.querySelector('.item-content');
            itemContent.textContent = newText;
            li.classList.remove('editing');
            
            // 編集アクション要素を削除
            const editActions = li.querySelector('.edit-actions');
            if (editActions) {
                editActions.remove();
            }
        } else {
            alert('更新に失敗しました');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('エラーが発生しました');
    });
}

// アイテム編集のキャンセル
function cancelEdit(li, originalText) {
    const itemContent = li.querySelector('.item-content');
    itemContent.textContent = originalText;
    li.classList.remove('editing');
    
    // 編集アクション要素を削除
    const editActions = li.querySelector('.edit-actions');
    if (editActions) {
        editActions.remove();
    }
}

// アイテムの削除
function deleteItem(pointType, itemIndex) {
    // プロジェクトIDの取得
    const urlParts = window.location.pathname.split('/');
    const projectId = urlParts[urlParts.length - 1];
    
    // サーバーに削除リクエストを送信
    const formData = new FormData();
    formData.append('point_type', pointType);
    formData.append('item_index', itemIndex);
    
    fetch(`/project/${projectId}/item/delete`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('削除に失敗しました');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('エラーが発生しました');
    });
}
