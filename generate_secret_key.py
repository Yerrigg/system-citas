"""
Script para generar una SECRET_KEY segura para Django
No requiere Django instalado
"""
import secrets
import string

def generate_secret_key(length=50):
    """Genera una SECRET_KEY segura"""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Generar una clave aleatoria segura
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == '__main__':
    print("=" * 70)
    print("SECRET_KEY GENERADA PARA PRODUCTION:")
    print("=" * 70)
    print(generate_secret_key())
    print("=" * 70)
    print("\n✅ Copia esta clave y úsala en Railway como variable de entorno")
    print("Variable: SECRET_KEY")
    print("Valor: La clave generada arriba\n")
