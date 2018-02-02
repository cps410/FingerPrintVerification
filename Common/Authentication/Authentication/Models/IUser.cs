using Common.Authentication.DBHandlers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Common.Authentication.Models
{
    public interface IUser
    {
        /// <summary>
        /// The data manager for the User model. This performs
        /// CRUD operations on the User table.
        /// </summary>
        IDbHandler<IUser> Objects { get; }

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