from persistencia.Mapper     import Mapper
from logica.PDF              import PDF
from logica.Audio            import Audio
from logica.Usefull          import Usefull

class System:
    @staticmethod
    def save(student):
        mapper   =Mapper(student)
        if mapper.exists(student.getIdentification()):
            mapper.update()
        else:
            mapper.save()
        recording=Audio()
        recording.createGreeting(student.fullName())
    
    @staticmethod
    def delete(identification):
        mapper   =Mapper(None)
        mapper.delete(identification)
    
    @staticmethod
    def list():
        mapper=Mapper(None)
        return mapper.listStudent()

    @staticmethod
    def opening(date):
        mapper=Mapper(None)
        if not mapper.isOpening(date):
            mapper.opening(date)

    @staticmethod
    def present(id,date):
        mapper=Mapper(None)
        return mapper.present(int(id),date)

    @staticmethod
    def isPresent(id,date):
        mapper=Mapper(None)
        return mapper.isPresent(int(id),date)
    
    @staticmethod
    def closing(date,closed):
        mapper=Mapper(None)
        return mapper.closing(date,closed)

    @staticmethod
    def wanting(date):
        mapper=Mapper(None)
        return mapper.wanting(date)

    @staticmethod
    def isWanting():
        mapper=Mapper(None)
        return mapper.isWanting()
    
    @staticmethod
    def lisPresentToday():
        mapper=Mapper(None)
        return mapper.presentToday(Usefull.today())
    
    @staticmethod
    def generarQR(identification):
        mapper=Mapper(None)
        student=mapper.find(identification)
        PDF.generar(student)

    @staticmethod
    def find(identification):
        if identification.isnumeric():
            mapper=Mapper(None)
            return mapper.find(int(identification))
        else:
            return None