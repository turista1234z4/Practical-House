# --- Build ---
FROM node:20-alpine AS builder

WORKDIR /app

# Copia apenas os arquivos essenciais primeiro (melhora cache do docker)
COPY package.json package-lock.json* ./

RUN npm install

# Agora copia o restante do projeto
COPY . .

# Executa o build de produção
RUN npm run build


# --- Etapa 2: Servir com Nginx ---
FROM nginx:alpine

# Remove o default e substitui pela nossa config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos buildados da etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
