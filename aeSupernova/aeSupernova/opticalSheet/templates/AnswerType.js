/**
  * class AnswerType
  * Represent a AnswerType in the database.
  */

    /**
     * Answer type name, as it is in the database.
     */
    //name 
    /**
     * Assossiated database id.
     */
    //idAnswerType 
    /**
     * A dict representing the meaning of the alternatives in the form:
     * {'A':'alternativeA', 'B':'alternativeB'...}
     */
    //alternativeMeaning 

/**
 * Initialization method.
 * @param name
    *      
 * @param idAnswerType
    *      
 * @param alternativeMeaning
    *      
 */
function AnswerType(name, idAnswerType, alternativeMeaning){
    this.name = name
    this.idAnswerType = idAnswerType
    this.alternativeMeaning = alternativeMeaning
}
