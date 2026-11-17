{{/* Спільні мітки всіх ресурсів діаграми */}}
{{- define "surveylab.labels" -}}
app.kubernetes.io/part-of: surveylab
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{/* Повне ім'я образу: реєстр/назва:тег (тег за замовчуванням — appVersion) */}}
{{- define "surveylab.image" -}}
{{- $tag := .root.Values.image.tag | default .root.Chart.AppVersion -}}
{{ .root.Values.image.registry }}/{{ .name }}:{{ $tag }}
{{- end }}

{{/* Ім'я служби бази даних */}}
{{- define "surveylab.dbHost" -}}
{{ .Release.Name }}-db
{{- end }}

{{/* Ім'я Secret з обліковими даними БД: власний (db.existingSecret) або створений діаграмою */}}
{{- define "surveylab.dbSecret" -}}
{{- default (printf "%s-db" .Release.Name) .Values.db.existingSecret -}}
{{- end -}}
