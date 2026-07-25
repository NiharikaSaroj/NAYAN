const API_URL = "http://127.0.0.1:8000";


async function checkBackend(){

    try{

        const response = await fetch(
            `${API_URL}/health`
        );


        const data = await response.json();


        console.log(
            "Backend:",
            data
        );


        return data;


    }
    catch(error){

        console.error(
            "Backend connection failed:",
            error
        );

        return null;

    }

}



async function askNayan(question){

    /*
       Future endpoint:

       POST /ask

       {
          "question":"..."
       }

    */


    try{


        const response = await fetch(
            `${API_URL}/ask`,
            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },


                body:JSON.stringify({

                    question:question

                })

            }
        );



        const data =
        await response.json();


        return data.answer;


    }
    catch(error){

        console.error(error);


        return "Backend is not connected yet.";

    }


}