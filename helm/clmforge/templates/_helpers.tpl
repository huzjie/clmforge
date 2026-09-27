{{- define "clmforge.fullname" -}}
{{- printf "%s-%s" .Release.Name "clmforge" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
