# FERRAMENTAS E ANALISE DE CUSTOS
## Ecossistema de Automacao INEMA.Make

---

## PLATAFORMAS DE AUTOMACAO

### Make.com (Principal)
| Plano | Operacoes | Custo |
|-------|-----------|-------|
| Free | 1.000/mes | $0 |
| Core | 10.000/mes | $9/mes |
| Pro | 10.000/mes | $16/mes |
| Teams | 10.000/mes | $29/mes |
| Enterprise | Ilimitado | $85+/mes |

**Observacoes:**
- Plano Pro recomendado para desenvolvedores
- Nao funciona em VPS (diferente do n8n)

### n8n (Alternativa Self-Hosted)
| Opcao | Custo |
|-------|-------|
| Cloud | $20+/mes |
| Self-hosted (VPS) | ~R$300/ano |

**Vantagens n8n:**
- Codigo aberto
- Hospedagem propria
- Sem limite de operacoes
- Mais transparente para debug

---

## LLMs E APIs DE IA

### OpenAI
| Modelo | Input | Output | Uso |
|--------|-------|--------|-----|
| GPT-4 Turbo | $10/M tokens | $30/M tokens | Principal |
| GPT-4o | $5/M tokens | $15/M tokens | Equilibrado |
| GPT-3.5 Turbo | $0.50/M tokens | $1.50/M tokens | Economico |
| text-embedding-3-small | $0.02/M tokens | - | RAG |

**Custo medio por workflow:** ~$0.02

### Claude (Anthropic)
| Item | Valor |
|------|-------|
| Creditos iniciais | $5 |
| Claude 3 Opus | $15/M input, $75/M output |
| Claude 3.5 Sonnet | $3/M input, $15/M output |
| Claude 3 Haiku | $0.25/M input, $1.25/M output |

### DeepSeek R1
| Item | Valor |
|------|-------|
| Input | $0.55/M tokens |
| Output | $2.19/M tokens |

**27x mais barato que OpenAI GPT-4!**

### Groq
| Item | Valor |
|------|-------|
| Free tier | Limitado |
| Modelos | Llama, Mixtral |

**Recomendado para:** Testes e prototipagem

### OpenRouter
| Item | Valor |
|------|-------|
| Taxa | Variavel por modelo |
| Vantagem | Acesso a multiplos LLMs |

---

## GERACAO DE IMAGENS

### DALL-E 3 (OpenAI)
| Resolucao | Custo |
|-----------|-------|
| 1024x1024 | $0.040 |
| 1024x1792 | $0.080 |
| 1792x1024 | $0.080 |

### Flux (Replicate)
| Item | Valor |
|------|-------|
| Por imagem | ~$0.003-0.05 |
| Qualidade | Superior ao DALL-E |

### Leonardo AI
| Plano | Custo |
|-------|-------|
| Free | 150 tokens/dia |
| Apprentice | $12/mes |
| Artisan | $30/mes |

---

## VOZ E AUDIO

### Eleven Labs
| Plano | Caracteres | Custo |
|-------|------------|-------|
| Free | 10.000/mes | $0 |
| Starter | 30.000/mes | $5/mes |
| Creator | 100.000/mes | $22/mes |
| Pro | 500.000/mes | $99/mes |

**Clone de voz:** Disponivel a partir do Creator

### Synthflow
| Item | Valor |
|------|-------|
| Por minuto | $0.58 |
| Uso | Agentes de voz |

### Retell AI
| Item | Valor |
|------|-------|
| Por minuto | $0.07-0.12 |
| Uso | Chamadas automaticas |

### VAPI
| Item | Valor |
|------|-------|
| Por minuto | $0.05+ |
| Uso | Voice API |

### Bland AI
| Item | Valor |
|------|-------|
| Por minuto | $0.09 |
| Uso | Ligacoes telefonicas |

### Adobe Podcast Enhance
| Item | Valor |
|------|-------|
| Uso | Gratuito |
| Funcao | Melhorar qualidade audio |

---

## INTEGRACAO E DADOS

### Airtable
| Plano | Registros | Custo |
|-------|-----------|-------|
| Free | 1.000 | $0 |
| Plus | 5.000 | $10/mes |
| Pro | 50.000 | $20/mes |

### Apify
| Plano | Custo |
|-------|-------|
| Free | $5 creditos/mes |
| Personal | $49/mes |
| Team | $499/mes |

**Uso:** Web scraping, raspagem redes sociais

### Pinecone (Vector DB)
| Plano | Custo |
|-------|-------|
| Starter | Gratuito |
| Standard | $0.00025/hora |

**Uso:** RAG, embeddings, busca semantica

---

## COMUNICACAO

### WhatsApp Business API
| Provedor | Custo |
|----------|-------|
| Z-API | R$49+/mes |
| Evolution API | Self-hosted |
| Twilio | $0.005/msg |

### Twilio (SMS/Voz)
| Servico | Custo |
|---------|-------|
| SMS | $0.0079/msg |
| Voz | $0.0085/min |
| Numero | $1/mes |

---

## HOSPEDAGEM E INFRAESTRUTURA

### VPS para n8n
| Provedor | Custo |
|----------|-------|
| DigitalOcean | $6/mes |
| Contabo | R$25/mes |
| Oracle Cloud | Gratuito (tier) |

### Dropbox
| Plano | Storage | Custo |
|-------|---------|-------|
| Basic | 2GB | Gratuito |
| Plus | 2TB | $11.99/mes |

---

## TABELA COMPARATIVA DE CUSTOS MENSAIS

### Setup Iniciante (Gratuito)
| Ferramenta | Custo |
|------------|-------|
| Make.com Free | $0 |
| Groq Free | $0 |
| Airtable Free | $0 |
| **Total** | **$0** |

### Setup Intermediario
| Ferramenta | Custo |
|------------|-------|
| Make.com Pro | $16 |
| OpenAI | ~$10 |
| Eleven Labs Starter | $5 |
| Airtable Free | $0 |
| **Total** | **~$31/mes** |

### Setup Profissional
| Ferramenta | Custo |
|------------|-------|
| Make.com Teams | $29 |
| OpenAI | ~$50 |
| Eleven Labs Creator | $22 |
| Apify Personal | $49 |
| Airtable Plus | $10 |
| **Total** | **~$160/mes** |

### Setup Agencia
| Ferramenta | Custo |
|------------|-------|
| Make.com Enterprise | $85 |
| OpenAI | ~$200 |
| Eleven Labs Pro | $99 |
| Retell AI | ~$100 |
| Apify Team | $499 |
| Airtable Pro | $20 |
| **Total** | **~$1.000/mes** |

---

## ALTERNATIVAS GRATUITAS DOCUMENTADAS

| Pago | Alternativa Gratuita |
|------|---------------------|
| OpenAI GPT-4 | Groq (Llama), DeepSeek |
| Make.com | n8n self-hosted |
| Airtable | Google Sheets |
| Eleven Labs | Edge TTS, gTTS |
| Apify | Puppeteer, Playwright |
| Pinecone | ChromaDB, FAISS |

---

## DICAS DE OTIMIZACAO DE CUSTOS

1. **Comece com tier gratuito** de todas as ferramentas
2. **Use DeepSeek R1** para tarefas que nao precisam de GPT-4
3. **Groq para prototipagem** antes de ir para producao
4. **Cache de respostas** para evitar chamadas repetidas
5. **Batch processing** para reduzir operacoes no Make
6. **n8n self-hosted** se tiver volume alto
7. **Google Sheets** como database gratuito
8. **Webhooks Groq** para chatbots de baixo custo

---

**Ultima atualizacao:** Janeiro 2026
