(function(){
	let items = [];
	let filtered = [];
	let sortKey = null;
	let sortDir = 1;
	let page = 1;
	let pageSize = 10;

	const $status = () => document.getElementById('status');
	const $tableBody = () => document.querySelector('#inventoryTable tbody');
	const $search = () => document.getElementById('search');
	const $pageSize = () => document.getElementById('pageSize');
	const $pagination = () => document.getElementById('pagination');

	function setStatus(text, isError){
		const el = $status();
		el.textContent = text || '';
		el.className = isError ? 'status error' : 'status';
	}

	async function fetchInventory(){
		setStatus('Loading inventory...');
		try{
			const res = await fetch('/inventory');
			if(!res.ok) throw new Error(res.statusText || 'Failed');
			const data = await res.json();
			items = Array.isArray(data) ? data : [];
			page = 1;
			applyFilters();
			setStatus('Loaded ' + items.length + ' items');
		}catch(err){
			setStatus('Error loading inventory: ' + err.message, true);
			items = [];
			applyFilters();
		}
	}

	function applyFilters(){
		const q = ($search().value || '').toLowerCase().trim();
		if(q){
			filtered = items.filter(it => {
				return (''+it.name).toLowerCase().includes(q)
					|| (''+it.sku).toLowerCase().includes(q)
					|| (''+it.location).toLowerCase().includes(q)
					|| (''+it.id).toLowerCase().includes(q);
			});
		} else filtered = items.slice();

		if(sortKey){
			filtered.sort((a,b) => {
				const av = a[sortKey] ?? '';
				const bv = b[sortKey] ?? '';
				if(typeof av === 'number' && typeof bv === 'number') return (av-bv)*sortDir;
				return String(av).localeCompare(String(bv)) * sortDir;
			});
		}
		renderTable();
		renderPagination();
	}

	function renderTable(){
		const tbody = $tableBody();
		tbody.innerHTML = '';
		pageSize = parseInt($pageSize().value,10) || 10;
		const start = (page-1)*pageSize;
		const pageItems = filtered.slice(start, start+pageSize);

		for(const it of pageItems){
			const tr = document.createElement('tr');
			tr.innerHTML = `
				<td>${escapeHtml(it.id)}</td>
				<td>${escapeHtml(it.name)}</td>
				<td>${escapeHtml(it.sku)}</td>
				<td>${escapeHtml(it.quantity)}</td>
				<td>${escapeHtml(it.location)}</td>
				<td>${escapeHtml(it.last_updated || '')}</td>
				<td>
					<button data-id="${escapeHtml(it.id)}" class="btn small view">View</button>
					<button data-id="${escapeHtml(it.id)}" class="btn small edit">Edit</button>
					<button data-id="${escapeHtml(it.id)}" class="btn small danger">Delete</button>
				</td>
			`;
			tbody.appendChild(tr);
		}
		// attach simple action handler only to view buttons (other buttons are UI-only for now)
		tbody.querySelectorAll('button.view').forEach(btn => {
			btn.addEventListener('click', () => {
				const id = btn.getAttribute('data-id');
				alert('Open item: ' + id);
			});
		});
	}

	function renderPagination(){
		const container = $pagination();
		container.innerHTML = '';
		const total = filtered.length;
		const pages = Math.max(1, Math.ceil(total / pageSize));

		const info = document.createElement('span');
		info.className = 'page-info';
		info.textContent = `Showing ${Math.min((page-1)*pageSize+1, total)}–${Math.min(page*pageSize, total)} of ${total}`;
		container.appendChild(info);

		const btnPrev = document.createElement('button');
		btnPrev.textContent = 'Prev';
		btnPrev.disabled = page <= 1;
		btnPrev.addEventListener('click', ()=> { page = Math.max(1, page-1); renderTable(); renderPagination(); });
		container.appendChild(btnPrev);

		const btnNext = document.createElement('button');
		btnNext.textContent = 'Next';
		btnNext.disabled = page >= pages;
		btnNext.addEventListener('click', ()=> { page = Math.min(pages, page+1); renderTable(); renderPagination(); });
		container.appendChild(btnNext);
	}

	function escapeHtml(v){
		if(v === null || v === undefined) return '';
		return String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[c]);
	}

	function addHeaderSorting(){
		document.querySelectorAll('#inventoryTable thead th[data-key]').forEach(th => {
			th.style.cursor = 'pointer';
			th.addEventListener('click', ()=>{
				const key = th.getAttribute('data-key');
				if(sortKey === key) sortDir = -sortDir; else { sortKey = key; sortDir = 1; }
				applyFilters();
			});
		});
	}

	function init(){
		document.getElementById('refresh').addEventListener('click', fetchInventory);
		$search().addEventListener('input', ()=>{ page = 1; applyFilters(); });
		$pageSize().addEventListener('change', ()=>{ page = 1; applyFilters(); });
		addHeaderSorting();
		fetchInventory();
	}

	document.addEventListener('DOMContentLoaded', init);

})();

