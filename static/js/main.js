const firstFocusable = container => {
    const target = container.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (target) {
        target.focus();
    }
};

const getScrollbarWidth = () => {
    const outer = document.createElement('div');
    outer.style.visibility = 'hidden';
    outer.style.overflow = 'scroll';
    document.body.appendChild(outer);
    const inner = document.createElement('div');
    outer.appendChild(inner);
    const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;
    if (outer.parentNode) {
        outer.parentNode.removeChild(outer);
    }
    if (document.body.scrollHeight > window.innerHeight) {
        return scrollbarWidth;
    }
    return 0;
};

class Modal {
    constructor(element) {
        this.template = element;

        this.escapeEvent = event => {
            if (event.key === 'Escape') {
                this.close();
            }
        };

        this.template.addEventListener('click', event => {
            if (event.target === this.template) {
                this.close();
            }
        });

        const closeButton = this.template.querySelector('.dialog-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.close();
            });
        }
    }

    open() {
        this.activeElement = document.activeElement;
        this.template.setAttribute('open', true);
        document.addEventListener('keydown', this.escapeEvent);
        document.body.style.overflow = 'hidden';
        document.body.style.paddingRight = getScrollbarWidth() + 'px';
        firstFocusable(this.template);
    }

    close() {
        this.template.removeAttribute('open');
        document.removeEventListener('keydown', this.escapeEvent);
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
        if (this.activeElement) {
            this.activeElement.focus();
        }
    }

}

(() => {
    document.querySelectorAll('[data-modal-open]').forEach(button => {
        const modalId = button.dataset.modalOpen;
        const modalElement = document.querySelector(`[data-modal="${modalId}"]`);
        if (modalElement) {
            const modal = new Modal(modalElement);
            button.addEventListener('click', () => {
                modal.open();
            });
        }
    });
})();
