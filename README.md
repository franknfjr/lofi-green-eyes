# Lofi Green Eyes

Process:

```
fly apps create lofi-green-eyes
```

```
fly deploy
```

```bash
curl -X POST "https://lofi-green-eyes.fly.dev/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"80s pop rock track with bassy drums and synth","duration": 30}' \
     --output musica_pop1.mp3
```
