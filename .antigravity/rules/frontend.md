# Diretrizes Arquiteturais: Frontend React/TS (Sisdoa)

1. **Tipagem Estrita (Inflexível):**
   - O uso do tipo `any` é explicitamente proibido.
   - Todas as respostas vindas de `/api/*` devem possuir uma `interface` TypeScript correspondente em `web/src/types/`.

2. **Gerenciamento de Estado de Servidor:**
   - É proibido usar `useEffect` em conjunto com `useState` para fazer fetch de dados da API.
   - Todas as chamadas HTTP (GET/POST/PUT/DELETE) devem ser envelopadas pelos hooks do `@tanstack/react-query` (`useQuery`, `useMutation`) para garantir cache e invalidação correta.

3. **Comunicação HTTP:**
   - O Axios é o cliente HTTP padrão. Uma instância global deve ser configurada em `web/src/services/api.ts` contendo a `baseURL` variando por ambiente (Localhost vs Vercel).

4. **Estilização e Componentização:**
   - Todo CSS deve ser feito exclusivamente via Tailwind CSS utility classes. Evite a criação de arquivos `.css` ou `.scss` paralelos.
   - Componentes devem ser puramente funcionais e aderir ao Single Responsibility Principle (SRP).
