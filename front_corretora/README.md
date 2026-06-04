# Front Corretora - Dashboard de Previsão

Interface web desenvolvida em React para consumir a API de previsão de faturamento da corretora Carro & Casa.

O dashboard permite enviar uma planilha comercial, consultar a API de previsão e visualizar os resultados em cards, gráfico e tabela.

---

## Funcionalidades

- Upload de planilha `.xlsx` ou `.csv`;
- Envio do arquivo para a API Flask;
- Exibição da previsão de faturamento por cenário;
- Visualização em gráfico de linha;
- Cards com menor previsão, previsão esperada média e maior previsão;
- Tabela detalhada com mês, cenário e faturamento previsto;
- Tratamento de carregamento e mensagens de erro.

---

## Tecnologias utilizadas

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- Recharts

---

## API utilizada

A aplicação consome a API deployada no Render:

```text
https://carro-casa-revenue-forecast.onrender.com/api/forecast
```

A rota espera uma requisição POST com multipart/form-data, usando o campo:

``` file ```

## Como rodar localmente
Acesse a pasta do front:

``` cd front_corretora ```

Instale as dependências:

``` npm install ```

Rode o projeto em ambiente de desenvolvimento:

```npm run dev ```

Gere a build de produção:

``` npm run build ```

Visualize a build localmente:

``` npm run preview ```

## Estrutura principal
```
front_corretora/
├── index.html
├── package.json
├── package-lock.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── src/
    └── routes/
        ├── index.tsx
        ├── main.tsx
        └── styles.css
```