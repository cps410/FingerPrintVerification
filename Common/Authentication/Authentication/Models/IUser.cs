using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Common.Models
{
    public interface IUser
    {
        /// <summary>
        /// Authenticates this user based on their fingerprint.
        /// </summary>
        /// <returns>
        /// true if the fingerprint matched that stored in the
        /// database.
        /// </returns>
        bool MatchFingerPrint(/*TODO: install scanner software*/);
    }
}