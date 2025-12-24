document.addEventListener('DOMContentLoaded', function() {

    const bookingForm = document.getElementById('bookingForm');
    const serviceSelect = document.getElementById('service');
    const masterSelect = document.getElementById('master');
    const dateInput = document.getElementById('date');
    const formMessage = document.getElementById('formMessage');
    function setMinDate() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');

        dateInput.min = `${year}-${month}-${day}`;
        dateInput.value = `${year}-${month}-${day}`;
    }

    setMinDate();

    serviceSelect.addEventListener('change', async function() {
        const serviceId = this.value;

        masterSelect.innerHTML = '<option value="">Загрузка...</option>';
        masterSelect.disabled = true;

        if (!serviceId) {
            masterSelect.innerHTML = '<option value="">Сначала выберите услугу</option>';
            return;
        }

        try {
            const response = await fetch(`/api/services/${serviceId}/masters/`);

            if (!response.ok) {
                throw new Error('Ошибка загрузки мастеров');
            }

            const masters = await response.json();
            masterSelect.innerHTML = '<option value="">Выберите мастера</option>';

            masters.forEach(master => {
                const option = document.createElement('option');
                option.value = master.id;
                option.textContent = `${master.name} (${master.specialization})`;
                masterSelect.appendChild(option);
            });

            masterSelect.disabled = false;
            if (masters.length === 0) {
                masterSelect.innerHTML = '<option value="">Нет доступных мастеров</option>';
            }

        } catch (error) {
            console.error('Ошибка:', error);
            masterSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
        }
    });

    const phoneInput = document.getElementById('client_phone');

    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');

        if (value.startsWith('8')) {
            value = '7' + value.slice(1);
        }
        if (value && !value.startsWith('7')) {
            value = '7' + value;
        }

        value = value.slice(0, 11);
        if (value) {
            e.target.value = '+' + value;
        }
    });

    bookingForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        hideMessage();
        const formData = {
            client_name: document.getElementById('client_name').value.trim(),
            client_phone: document.getElementById('client_phone').value.trim(),
            client_email: document.getElementById('client_email').value.trim(),
            service: parseInt(serviceSelect.value),
            master: parseInt(masterSelect.value),
            date: dateInput.value,
            time: document.getElementById('time').value,
            comment: document.getElementById('comment').value.trim()
        };

        if (!validateForm(formData)) {
            return;
        }

        const submitBtn = bookingForm.querySelector('.btn-submit');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch('/api/appointments/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                showMessage('success', result.message);

                bookingForm.reset();
                setMinDate();
                masterSelect.innerHTML = '<option value="">Сначала выберите услугу</option>';

            } else {
                let errorMessage = 'Произошла ошибка. Попробуйте ещё раз.';

                if (result.errors) {
                    const errorList = [];
                    for (const [field, messages] of Object.entries(result.errors)) {
                        if (Array.isArray(messages)) {
                            errorList.push(...messages);
                        } else {
                            errorList.push(messages);
                        }
                    }
                    errorMessage = errorList.join(' ');
                }

                showMessage('error', errorMessage);
            }

        } catch (error) {
            console.error('Ошибка отправки:', error);
            showMessage('error', 'Ошибка соединения. Проверьте интернет и попробуйте снова.');

        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });

    function validateForm(data) {
        const errors = [];

        if (!data.client_name) {
            errors.push('Введите ваше имя');
        }

        if (!data.client_phone || data.client_phone.length < 12) {
            errors.push('Введите корректный номер телефона');
        }

        if (!data.service) {
            errors.push('Выберите услугу');
        }

        if (!data.master) {
            errors.push('Выберите мастера');
        }

        if (!data.date) {
            errors.push('Выберите дату');
        }

        if (!data.time) {
            errors.push('Выберите время');
        }

        if (errors.length > 0) {
            showMessage('error', errors.join('. '));
            return false;
        }

        return true;
    }

    function showMessage(type, message) {
        formMessage.textContent = message;
        formMessage.className = 'form-message ' + type;
        formMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideMessage() {
        formMessage.className = 'form-message';
        formMessage.textContent = '';
    }

    console.log('📝 Форма записи инициализирована');
});

