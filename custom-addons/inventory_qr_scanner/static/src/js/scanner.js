document.addEventListener('DOMContentLoaded', function() {
    
    class QRScanner {
        constructor() {
            this.sessionData = window.sessionData || {};
            this.currentLocationId = this.sessionData.current_location_id || null;
            
            this.initElements();
            this.bindEvents();
        }
        
        initElements() {
            this.manualInput = document.getElementById('manual-input');
            this.processBtn = document.getElementById('process-manual');
            this.finishBtn = document.getElementById('finish-session');
            this.messagesDiv = document.getElementById('messages');
            this.scansDiv = document.getElementById('scans-list');
            this.locationSelect = document.getElementById('location-select');
            this.currentLocationDiv = document.getElementById('current-location');
        }
        
        bindEvents() {
            if (this.processBtn) {
                this.processBtn.addEventListener('click', () => this.processManual());
            }
            
            if (this.manualInput) {
                this.manualInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.processManual();
                    }
                });
            }
            
            if (this.locationSelect) {
                this.locationSelect.addEventListener('change', (e) => this.setLocation(e.target.value));
            }
            
            if (this.finishBtn) {
                this.finishBtn.addEventListener('click', () => this.finishSession());
            }
        }
        
        processManual() {
            const code = this.manualInput.value.trim();
            if (!code) {
                this.showMessage('Please enter a code', 'error');
                return;
            }
            
            this.processCode(code);
            this.manualInput.value = '';
        }
        
        async processCode(code) {
            try {
                this.showMessage('Processing...', 'info');
                
                const response = await fetch('/inventory/scan/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            code: code,
                            session_id: this.sessionData.session_id,
                            location_id: this.currentLocationId,
                            quantity: 1
                        }
                    })
                });
                
                const result = await response.json();
                const data = result.result || result;
                
                if (data.success) {
                    this.showMessage(data.message, 'success');
                    
                    if (data.type === 'location') {
                        this.currentLocationId = data.location_id;
                        this.updateLocation(data.location_name);
                    } else if (data.type === 'product') {
                        this.addScan(data);
                    }
                } else {
                    this.showMessage(data.message, 'error');
                }
                
            } catch (error) {
                console.error('Process error:', error);
                this.showMessage('Network error: ' + error.message, 'error');
            }
        }
        
        async setLocation(locationId) {
            if (!locationId) return;
            
            try {
                const response = await fetch(`/inventory/scan/location/${locationId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            session_id: this.sessionData.session_id
                        }
                    })
                });
                
                const result = await response.json();
                const data = result.result || result;
                
                if (data.success) {
                    this.currentLocationId = parseInt(locationId);
                    this.updateLocation(data.location_name);
                    this.showMessage(data.message, 'success');
                }
                
            } catch (error) {
                console.error('Location error:', error);
            }
        }
        
        async finishSession() {
            if (confirm('Finish this scanning session?')) {
                try {
                    const response = await fetch(`/inventory/scan/finish/${this.sessionData.session_id}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            jsonrpc: '2.0',
                            method: 'call',
                            params: {}
                        })
                    });
                    
                    const result = await response.json();
                    const data = result.result || result;
                    
                    if (data.success) {
                        this.showMessage('Session finished!', 'success');
                        setTimeout(() => {
                            window.location.href = '/inventory/scan';
                        }, 2000);
                    }
                    
                } catch (error) {
                    console.error('Finish error:', error);
                }
            }
        }
        
        updateLocation(locationName) {
            if (this.currentLocationDiv) {
                this.currentLocationDiv.textContent = locationName;
                this.currentLocationDiv.classList.remove('text-muted');
            }
        }
        
        showMessage(message, type = 'info') {
            if (!this.messagesDiv) return;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.innerHTML = `
                <div class="d-flex justify-content-between">
                    <span>${message}</span>
                    <small>${new Date().toLocaleTimeString()}</small>
                </div>
            `;
            
            this.messagesDiv.insertBefore(messageDiv, this.messagesDiv.firstChild);
            
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 5000);
        }
        
        addScan(scanData) {
            if (!this.scansDiv) return;
            
            const scanDiv = document.createElement('div');
            scanDiv.className = 'scan-item';
            
            scanDiv.innerHTML = `
                <div class="scan-info">
                    <div class="scan-product">${scanData.product_name}</div>
                    <div class="scan-location">📍 ${scanData.location_name}</div>
                    <div class="scan-time">${new Date().toLocaleTimeString()}</div>
                </div>
                <div class="scan-quantity">${scanData.quantity}</div>
            `;
            
            this.scansDiv.insertBefore(scanDiv, this.scansDiv.firstChild);
        }
    }
    
    if (window.sessionData) {
        window.qrScanner = new QRScanner();
        
        window.testScan = function(code) {
            if (window.qrScanner) {
                window.qrScanner.processCode(code);
            }
        };
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey) {
            switch(e.key) {
                case 'L':
                    e.preventDefault();
                    window.testScan('LOC:WH/Stock');
                    break;
                case 'P':
                    e.preventDefault();
                    window.testScan('PROD001');
                    break;
            }
        }
    });
});
