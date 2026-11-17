# Ansible для SurveyLab (етап 5 плану)

Ролі: `common` (пакети, користувач), `docker` (Docker і Compose), `surveylab`
(docker-compose.yml і .env із шаблонів, запуск стеку), `nginx_proxy`
(зворотний проксі), `monitoring` (node_exporter для Prometheus).

Секрети (пароль БД) — у `group_vars/all/vault.yml`, зашифрованому
`ansible-vault`. Пароль від сховища не зберігається в репозиторії: локально —
`export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible-lab/vault_pass`, у CI — секрет `ANSIBLE_VAULT_PASSWORD`.

```bash
cd infra/ansible
ansible-playbook site.yml --syntax-check
ansible-playbook site.yml --check
ansible-playbook site.yml
```

Production: `-i inventory/production.ini`; розгортання в CI — workflow
`ansible.yml` із ручним підтвердженням (середовище `production`).
