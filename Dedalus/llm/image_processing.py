from PIL import Image, ExifTags
from .config import vision_model  # Importar el modelo de visión

def process_image(image_file):
    """Procesa y analiza una imagen"""
    try:
        supported_formats = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
        file_extension = image_file.name.lower().split('.')[-1]

        if file_extension not in supported_formats:
            return f"Formato no soportado: {file_extension}. Usa: {', '.join(supported_formats)}"

        image = Image.open(image_file)

        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')

        metadata = ""
        try:
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    metadata += f"{tag_name}: {value}\n"
        except AttributeError:
            metadata = "No se encontraron metadatos EXIF."

        result = vision_model(image)
        description = result[0]['generated_text']

        return f"""
        **📷 Análisis de imagen**
        - 📏 Dimensiones: {image.width}x{image.height}
        - 📂 Formato: {file_extension.upper()}
        - 📝 Descripción generada: {description}
        - 📑 Metadatos EXIF: {metadata}
        """
    
    except Exception as e:
        return f"❌ Error procesando la imagen: {str(e)}"
