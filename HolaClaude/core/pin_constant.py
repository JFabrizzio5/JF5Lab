"""
PIN hardcoded. No removible via API.

PIN plano: 23052005
Hash bcrypt $2b$12 compilado.

startup_guard verifica que env HOLACLAUDE_PIN_HASH coincida con este
hash. Si alguien edita env, servicio falla al arrancar.
"""

PIN_HASH_HARDCODED = "$2b$12$Kf76/waTMkT/10/k1qB2pOa0OFKACaXL9DqeZvQ/J.UP3FCC6I.oO"
PIN_LENGTH = 8
