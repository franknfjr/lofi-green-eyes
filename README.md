# Lofi Green Eyes

Process:

```
fly apps create lofi-green-eyes
```

```
fly ips allocate-v4 --shared
```

```
fly deploy --flycast
```

```bash
curl -X POST "https://lofi-green-eyes.fly.dev/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"lofi hip hop with style of tecno brega from belém of pará","duration":10}' \
     --output musica_lofi.mp3
```
