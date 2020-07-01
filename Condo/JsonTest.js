//------------CREATE DUBLICATES OF THE RATEPLANS

const getToken = async () => {
    let response = await fetch('https://identity.apaleo.com/connect/token', 
    {
        method: 'POST',
        data: {
            'grant_type': 'client_credentials'
        },
        headers: {
            'Authorization': 'Basic VU5QVy1TUC1ISUVLS0E6d2toVXNEVUpZaFY0dUo3cWNGMkFlSDJuYzdRS3FV',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }
    )
    let data = await response.json()
    let resp = data.access_token
}

const token = getToken()

let ratePlanInfo = {};
/* const includedServices = (inclServ) => {
    for (let i = 0; i < inclServ.length; i++) {
        const id = inclServ[i].service.id;
        const grossPrice = inclServ[i].grossPrice;
        
    }
} */

const getRatePlans = async () => {
    let resp = [];
    let response = await fetch('https://api.apaleo.com/rateplan/v1/rate-plans', 
    {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    }
    )
    let data = await response.json()
    resp = data.ratePlans
    //ratePlanInfo = resp;

    for (let index = 0; index < resp.length; index++) {
        const ratePlanInfo = resp[index];



    const tsd = () => {
        if(ratePlanInfo.property.id == 'MUC') {
            return "MUC-BSK"
        } else if(ratePlanInfo.property.id == 'BER') {
            return "BER-TTD"
        }else if(ratePlanInfo.property.id == 'LND') {
            return "LND-MIT"
        }
    }
    const name = () => {
        if(ratePlanInfo.name.en == null) {
            return {"en": ratePlanInfo.name, "de": "Beispiel"}
        } else if(ratePlanInfo.name.en != null) {
            return {"en": ratePlanInfo.name.en, "de": "Beispiel"}
        } else if(ratePlanInfo.name.en != null && ratePlanInfo.name.de != null){
            return ratePlanInfo.name
        }
    }
    const desc = () => {
        if(ratePlanInfo.description.en == null) {
            return {"en": ratePlanInfo.description, "de": "Beispiel"}
        } else if(ratePlanInfo.description.en != null) {
            return {"en": ratePlanInfo.description.en, "de": "Beispiel"}
        } else if(ratePlanInfo.description.en != null && ratePlanInfo.description.de != null){
            return ratePlanInfo.description
        }
    }

    let copiedRatePlan = 
    {
        "code": ratePlanInfo.code + 'NEW', //Mandatory
        "propertyId": ratePlanInfo.property.id,//Mandatory
        "unitGroupId": ratePlanInfo.unitGroup.id,//Mandatory
        "cancellationPolicyId": ratePlanInfo.cancellationPolicy.id,//Mandatory
        "channelCodes": ratePlanInfo.channelCodes,//Mandatory
        "serviceType": ratePlanInfo.serviceType || "Accommodation",//Mandatory
        "vatType": ratePlanInfo.vatType || "Reduced",//Mandatory
        "isSubjectToCityTax": ratePlanInfo.isSubjectToCityTax,//Mandatory

        //-------------Must be found with corresponding Property ID (add first all TSD's)
        //------------"MUC-BSK" || "BER-TTD" || "LND-MIT",
        "timeSliceDefinitionId": tsd(),

        "name": name(),//Mandatory (also translations de if MUC/BER)
        "description": desc(),//Mandatory (also translations de if MUC/BER)
        "minGuaranteeType": ratePlanInfo.minGuaranteeType,//Mandatory
        "bookingPeriods": ratePlanInfo.bookingPeriods,
        "restrictions": ratePlanInfo.restrictions,
        // ---------------Pricing rule not mandatory for POST-operation.
        /* "pricingRule": {
          "baseRatePlanId": ratePlanInfo.pricingRule.baseRatePlan.id, // ----------must be with the same TSD as in the baserate
          "type": ratePlanInfo.pricingRule.type,
          "value": ratePlanInfo.pricingRule.value
        }, */
        "surcharges": ratePlanInfo.surcharges,
        "ageCategories": ratePlanInfo.ageCategories,
        "includedServices": ratePlanInfo.includedServices,
        "subAccountId": ratePlanInfo.subAccountId,
        //Optional
        /* "promoCodes": [
            "APA55100",
            "DISCOUNT20"
          ], */
      };
      console.log(copiedRatePlan)
      document.getElementById('main').innerHTML=JSON.stringify(copiedRatePlan);
    }

      /* await fetch('https://api.apaleo.com/rateplan/v1/rate-plans', 
        {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(copiedRatePlan)
        }
        ) */
}
getRatePlans() 