document.addEventListener('DOMContentLoaded', () => {
    const toolsGrid = document.getElementById('toolsGrid');
    const searchInput = document.getElementById('toolSearch');
    const catBtns = document.querySelectorAll('.cat-btn');
    const toolModal = document.getElementById('toolModal');
    const closeModal = document.getElementById('closeModal');
    const modalBody = document.getElementById('modalBody');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const loadMoreContainer = document.getElementById('loadMoreContainer');

    let allTools = [];
    let filteredTools = [];
    let itemsToShow = 16;
    let isSearching = false;

    // Function to fetch tools from Flask API
    async function fetchTools() {
        try {
            const res = await fetch('/api/tools');
            allTools = await res.json();
            filteredTools = [...allTools];
            renderTools();
            updateLiveStats(); // Update stats after loading tools
        } catch (error) {
            console.error('Error fetching tools:', error);
            if (toolsGrid) toolsGrid.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">Error loading tools. Please run the Flask server.</p>';
        }
    }

    // Function to update Live Stats from Backend
    async function updateLiveStats() {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();
            
            const toolStat = document.querySelector('.stat-number[data-target="100"]');
            const userStat = document.querySelector('.stat-number[data-target="50000"]');
            
            if (toolStat) {
                toolStat.setAttribute('data-target', data.toolCount);
                animateCounter(toolStat, data.toolCount);
            }
            
            if (userStat) {
                userStat.setAttribute('data-target', data.userCount);
                animateCounter(userStat, data.userCount, true);
            }
        } catch (err) {
            console.error('Error fetching stats:', err);
        }
    }

    function animateCounter(el, target, isLive = false) {
        let count = 0;
        const increment = target / 100;
        const update = () => {
            if (count < target) {
                count += increment;
                el.innerText = Math.ceil(count) + (isLive ? "" : "+");
                setTimeout(update, 20);
            } else {
                el.innerText = target + "+";
                if (isLive) {
                    // Start fluctuation for live users
                    setInterval(() => {
                        const variation = Math.floor(Math.random() * 20) - 10;
                        const current = parseInt(el.innerText);
                        el.innerText = (current + variation) + "+";
                    }, 3000);
                }
            }
        };
        update();
    }

    // Function to render tool cards
    function renderTools(isAppend = false) {
        if (!toolsGrid) return;
        
        if (!isAppend) toolsGrid.innerHTML = '';
        
        const toolsToDisplay = isSearching ? filteredTools : filteredTools.slice(0, itemsToShow);
        
        if (toolsToDisplay.length === 0) {
            toolsGrid.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">No tools found matching your criteria.</p>';
            if (loadMoreContainer) loadMoreContainer.style.display = 'none';
            return;
        }

        const startIndex = isAppend ? (itemsToShow - 16) : 0;
        const currentSlice = isSearching ? toolsToDisplay : toolsToDisplay.slice(startIndex);

        currentSlice.forEach((tool, index) => {
            const card = document.createElement('div');
            card.className = 'tool-card animate';
            card.style.animationDelay = `${(index % 10) * 0.05}s`;
            card.innerHTML = `
                <img src="${tool.img}" alt="${tool.name}" class="tool-image">
                <div class="tool-footer">
                    <span class="tool-tag">${tool.tag}</span>
                </div>
                <h3>${tool.name}</h3>
                <p>${tool.desc}</p>
                <div class="tool-footer">
                    <div class="tool-actions">
                        <button class="btn btn-outline btn-sm" onclick="openToolDetail('${tool.name}')">Learn More</button>
                        <a href="${tool.link}" target="_blank" class="btn btn-primary btn-sm">Use Tool</a>
                    </div>
                </div>
            `;
            toolsGrid.appendChild(card);
        });

        if (loadMoreContainer) {
            if (isSearching || itemsToShow >= filteredTools.length) {
                loadMoreContainer.style.display = 'none';
            } else {
                loadMoreContainer.style.display = 'block';
            }
        }
    }

    // Load More Logic
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            itemsToShow += 16;
            renderTools(true);
        });
    }

    // Modal Logic
    window.openToolDetail = (name) => {
        const tool = allTools.find(t => t.name === name);
        if (!tool) return;

        modalBody.innerHTML = `
            <div style="display: flex; gap: 2rem; align-items: flex-start; margin-bottom: 2rem;">
                <img src="${tool.img}" style="width: 120px; height: 120px; border-radius: 24px; object-fit: cover;">
                <div>
                    <h2 style="font-size: 2.5rem; margin-bottom: 0.5rem;">${tool.name}</h2>
                    <span class="tool-tag">${tool.tag}</span>
                </div>
            </div>
            <div style="background: var(--bg-dark); padding: 2rem; border-radius: 24px; margin-bottom: 2rem;">
                <h4 style="color: var(--primary); margin-bottom: 1rem;"><i class="fas fa-info-circle"></i> What is ${tool.name}?</h4>
                <p style="color: var(--text-muted); line-height: 1.8;">${tool.desc} It is one of the most powerful tools in the ${tool.tag} category, helping users achieve high-quality results efficiently.</p>
            </div>
            <h4 style="margin-bottom: 1.5rem;"><i class="fas fa-list-ol"></i> How to use this tool:</h4>
            <ul class="how-to-use-list">
                <li><span class="step-num">1</span> Click on the "Use Tool" button to visit the official ${tool.name} website.</li>
                <li><span class="step-num">2</span> Create an account or sign in to access the dashboard.</li>
                <li><span class="step-num">3</span> Input your requirements (text prompt, image, or file) into the provided interface.</li>
                <li><span class="step-num">4</span> Let the AI process your request and download or export your results instantly.</li>
            </ul>
        `;
        if (toolModal) {
            toolModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeModalFunc = () => {
        if (toolModal) {
            toolModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };

    if (closeModal) {
        closeModal.addEventListener('click', closeModalFunc);
    }

    window.addEventListener('click', (e) => {
        if (e.target === toolModal) closeModalFunc();
    });

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            isSearching = searchTerm.length > 0;
            
            filteredTools = allTools.filter(tool => 
                tool.name.toLowerCase().includes(searchTerm) || 
                tool.desc.toLowerCase().includes(searchTerm) ||
                tool.tag.toLowerCase().includes(searchTerm)
            );
            
            itemsToShow = 16;
            renderTools();
        });
    }

    // Category filtering
    catBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            catBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const category = btn.getAttribute('data-category');
            isSearching = false;
            searchInput.value = '';
            
            if (category === 'all') {
                filteredTools = [...allTools];
            } else {
                filteredTools = allTools.filter(tool => tool.category === category);
            }
            
            itemsToShow = 16;
            renderTools();
        });
    });

    // Header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '1rem 5%';
            header.style.background = 'rgba(2, 6, 23, 0.95)';
        } else {
            header.style.padding = '1.5rem 5%';
            header.style.background = 'var(--glass)';
        }
    });

    // Initial fetch
    fetchTools();
});
