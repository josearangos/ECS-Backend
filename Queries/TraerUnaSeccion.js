//obtener x seccion de formulario
db.getCollection("formAnswer").find(

   {
     "ECN" : "8243597212", 
    "CFN" : "2746674653",
     "Confirmado" : false
          
   },
   {
    seccion: {
                $elemMatch: {
                     number: 3
               }
      },_id:0
    }

)
